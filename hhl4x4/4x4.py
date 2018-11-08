# ======================================================================
# Copyright CERFACS (November 2018)
# Contributor: Adrien Suau (suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================


"""Implements the HHL algorithm describer in https://arxiv.org/abs/1110.2232v2.


"""

import copy

import numpy as np
import qiskit
import scipy.linalg as la
from sympy import pi

import hhl4x4.utils.endianness as endian
import hhl4x4.custom_gates.comment
import hhl4x4.custom_gates.hhl4x4
import hhl4x4.custom_gates.qpe


def postselect(statevector: np.ndarray, qubit_index: int, value: bool):
    mask = 1 << qubit_index
    if value:
        array_mask = np.arange(len(statevector)) & mask
    else:
        array_mask = not (np.arange(len(statevector)) & mask)

    def normalise(vec: np.ndarray):
        from scipy.linalg import norm
        return vec / norm(vec)

    return normalise(statevector[array_mask != 0])


def round_to_zero(vec: np.ndarray, tol=2e-15):
    vec.real[abs(vec.real) < tol] = 0.0
    vec.imag[abs(vec.imag) < tol] = 0.0
    return vec


def reverse_endianness(i: int, length: int) -> int:
    return int(''.join(reversed(('{0:0' + str(length) + 'b}').format(i))), 2)


def main():
    qancilla = endian.QRegisterBE(qiskit.QuantumRegister(1))
    qclock = endian.QRegisterBE(qiskit.QuantumRegister(4))
    qb = endian.QRegisterBE(qiskit.QuantumRegister(2))
    classical = endian.CRegister(qiskit.ClassicalRegister(1))

    circuit = qiskit.QuantumCircuit(qancilla, qclock, qb, classical)

    # 0. Initialise b
    circuit.comment("[4x4] Initialising b.")
    circuit.h(qb)
    circuit.comment("[4x4] Initialisation done!")

    # 1. Quantum Phase Estimation
    def controlled_hamiltonian_powers(n: int, circuit, control, target):
        # Previous method: just applying an optimized hamiltonian an exponential
        # number of times.
        # for i in range(2**n):
        #     #circuit.hamiltonian4x4(control, target).inverse()
        #     circuit.hamiltonian4x4(control, target)

        # Hard-coded values obtained thanks to optimise_parameters.py
        # The error (2-norm of the difference between the unitary matrix of the
        # quantum circuit and the true matrix) is bounded by 1e-7, no matter the
        # value of n.
        power = 2 ** n
        if power == 1:
            params = [0.19634953, 0.37900987, 0.9817477, 1.87900984, 0.58904862]
        elif power == 2:
            params = [1.9634954, 1.11532058, 1.9634954, 2.61532069, 1.17809726]
        elif power == 4:
            params = [-0.78539816, 1.01714584, 3.92699082, 2.51714589,
                      2.35619449]
        elif power == 8:
            params = [-9.01416169e-09, -0.750000046, 1.57079632, 0.750000039,
                      -1.57079633]
        else:
            raise NotImplementedError(
                "You asked for a non-implemented power: {}".format(power))
        circuit.hamiltonian4x4(control, target, params)

    circuit.comment("[4x4] 1. Quantum phase estimation.")
    qpe_gate = circuit.qpe(qclock, qb, controlled_hamiltonian_powers)

    ## 2. Phase rotation controlled by the eigenvalue.
    circuit.comment("[4x4] Inverting computed eigenvalues.")
    circuit.swap(qclock[1], qclock[2])

    # r is a parameter of the circuit.
    # A good value is between 5 and 6 according to the article.
    r = 6
    circuit.comment("[4x4] 2. Phase rotation.")

    def cry(circuit, theta, ctrl, target):
        circuit.comment("CRY")
        # Apply the supposed c-RY operation.
        circuit.cu3(theta, 0, 0, ctrl, target)

    for i in range(len(qclock)):
        cry(circuit, 2 ** (len(qclock) - i - r) * pi,
            qclock[len(qclock) - 1 - i], qancilla[0])

    circuit.comment("Inverting the inversion of eigenvalues.")
    circuit.swap(qclock[1], qclock[2])

    ## 3. Uncompute the Quantum Phase Estimation.
    circuit.comment("[4x4] 3. Inverting quantum phase estimation.")
    circuit._attach(copy.deepcopy(qpe_gate).inverse())

    circuit_no_measure = copy.deepcopy(circuit)

    ## 4. Measure the ancilla qubit to check.
    circuit.comment("[4x4] 4. Measurement.")
    circuit.measure(qancilla, classical)

    with open('4x4.qasm', 'w') as f:
        f.write(circuit.qasm())

    qasm_sim = qiskit.Aer.get_backend('qasm_simulator')
    state_sim = qiskit.Aer.get_backend('statevector_simulator')
    unitary_sim = qiskit.Aer.get_backend('unitary_simulator')

    # res_qasm = execute([circuit], qasm_sim, shots=10**5).result()
    # counts = res_qasm.get_counts()
    # filtered_counts = {key: counts[key] for key in counts if key[-1] == '1'}
    # significant_counts = {key: counts[key] for key in counts if counts[key]
    #  > 100}
    # significant_filtered_counts = {key: filtered_counts[key]
    #                                for key in filtered_counts
    #                                if filtered_counts[key] > 5000}
    # print("Counts:", counts, sep='\n')

    res_state = qiskit.execute([circuit_no_measure], state_sim).result()
    full_state = res_state.get_statevector()

    # The obtained full state is encoded with Qiskit's register order which
    # is not
    # the order we want. We need to change the array so that we reverse the
    # order of each register.
    size = full_state.shape[0]
    full_state_reversed = np.zeros((size,), dtype=full_state.dtype)
    for i in range(size):
        qubit_ancilla_value = i & 0b1
        qubit_clock_value = (i >> 1) & 0b1111
        qubit_b_value = (i >> 5) & 0b11
        reversed_regs_id = qubit_b_value | (qubit_clock_value << 2) | (
            qubit_ancilla_value << 6)
        full_state_reversed[reversed_regs_id] = full_state[i]
    full_state = full_state_reversed

    # full_state = reverse_indices_endianness(full_state)
    statevector = round_to_zero(postselect(full_state, 6, True), 1e-3)

    solution = np.sqrt(340) * statevector[:4]
    x_exact = np.array([-1, 7, 11, 13])

    print("Exact solution: {}".format(x_exact))
    print("Experimental solution: {}".format(solution))
    print("Error in found solution: {}".format(la.norm(solution - x_exact)))

    # res_unitary = execute([circuit_no_measure], unitary_sim,
    # skip_translation=skip).result()
    # unitary = res_unitary.get_unitary()
    # print("Unitary matrix:", unitary, sep='\n')

    amplitudes = np.absolute(full_state) ** 2

    X = np.arange(len(full_state))
    import matplotlib.pyplot as plt

    plt.bar(X, np.real(full_state))
    plt.xticks(np.arange(0, len(X) + 1, 2),
               [' '.join([bin(n)[3], bin(n)[4:8], bin(n)[8:10]]) for n in
                np.arange(len(X), 2 * len(X), 2)], usetex=False,
               rotation='vertical')
    plt.grid(zorder=0)
    plt.show()  # plot_histogram(counts)


if __name__ == '__main__':
    main()
