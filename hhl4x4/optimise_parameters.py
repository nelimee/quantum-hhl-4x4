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

"""Script used to find the best parameters for the Hamiltonian simulation.

The paper of Cao et al. (https://arxiv.org/abs/1110.2232v2) introduce an
Hamiltonian decomposition for their specific matrix. In this paper, they
also say that the circuit simulating the powers of the simulated
Hamiltonian can be obtained by multiplying the numeric parameters of 5
gates by a constant. After trying, it seems that this technique does not
work.
The method used here is not based on a mathematical analysis and its
convergence has not been studied. In other words, the fact that the
different powers of the Hamiltonian could be expressed just by changing
the coefficients of the circuit given in the paper of Cao et al. has
only been verified experimentally.
"""

import typing
import qiskit
import numpy as np
import scipy.linalg as la

import hhl4x4.custom_gates.hhl4x4

QubitType = typing.Tuple[qiskit.QuantumRegister, int]


def hamiltonian_error(power: int, display_digit: int):
    """Generate and return a function that will be given to the optimiser.

    The returned function will compute the error between the ideal unitary
    matrix (raised to the given power) and the simulated one with the set
    a parameters given by the optimizer.https://arxiv.org/abs/1110.2232v2

    :param power: the power we want to simulate.
    """

    def ret(params: typing.Sequence[float]) -> float:
        """Computes the error between the ideal matrix and the simulated one.

        :param params: parameters used in the quantum circuit.
        :return: the 2-norm distance between the ideal matrix and the simulated
        one.
        """
        list_format = ','.join(
            ["{: ." + str(display_digit) + "f}" for i in range(len(params))])
        print(("Computing U^{:<2} error with [" + list_format + "]: ").format(
            2 ** power, *params), end='')

        def swap(U):
            """Change the quantum gate representation.

            Qiskit uses a different endianness which change the unitary matrices
            representing quantum gates. This function takes a quantum gate "as
            we are used to represent them" and transform it "as Qiskit
            represents them".

            :param U: the matrix to change.
            :return: the adapted matrix.
            """
            from copy import deepcopy
            cpy = deepcopy(U)
            cpy[[1, 2], :] = cpy[[2, 1], :]
            cpy[:, [1, 2]] = cpy[:, [2, 1]]
            return cpy

        ancilla = qiskit.QuantumRegister(1)
        b = qiskit.QuantumRegister(2)
        classical = qiskit.ClassicalRegister(1)

        circuit = qiskit.QuantumCircuit(ancilla, b, classical)

        circuit.hamiltonian4x4(ancilla[0], b, params).inverse()

        unitary_sim = qiskit.Aer.get_backend('unitary_simulator')
        res = qiskit.execute([circuit], unitary_sim).result()
        unitary = res.get_unitary()

        A = .25 * np.array(
            [[15, 9, 5, -3], [9, 15, 3, -5], [5, 3, 15, -9], [-3, -5, -9, 15]])
        t0 = 2 * np.pi
        expA = swap(la.expm(-1.j * A * t0 * (2 ** power / 16)))
        unit = unitary[1::2, 1::2]
        np.set_printoptions(precision=2)
        err = la.norm(unit - expA)
        print("{: g}".format(err), end='\r', flush=True)
        return err

    return ret


def main():
    # Optimise!
    import scipy.optimize as opt
    import argparse

    parser = argparse.ArgumentParser(
        description='Find the optimum parameters for Hamiltonian simulation.')
    # parser.add_argument('--precision', default=1e-7, type=float,
    #                     help="Desired precision for the final Hamiltonian.")
    parser.add_argument("--maxiter", type=int, default=1000,
                        help="Maximum number of iterations (default to 1000).")
    parser.add_argument("--display-precision", type=int, default=8,
                        help="Number of digits needed when the parameters are "
                             "displayed (default to 8).")
    args = parser.parse_args()

    for power in range(4):
        opt_res = opt.minimize(hamiltonian_error(power, args.display_precision),
                               [0.2, 0.38, 0.98, 1.88, 0.59],
                               options={"maxiter": args.maxiter})
        print()


if __name__ == '__main__':
    main()
