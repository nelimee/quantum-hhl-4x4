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

"""This module contains functions to apply a controlled-Hamiltonian.
"""

from typing import Tuple, Union, List
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
from hhl4x4.custom_gates import comment, ccz, crx, csqtrx, crzz

QubitType = Tuple[QuantumRegister, int]


class Hamiltonian4x4Gate(CompositeGate):

    def __init__(self, ctrl: QubitType, targets: Tuple[QubitType],
                 params: List[float] = None, circuit: QuantumCircuit = None):
        """Initialize the Hamiltonian4x4Gate class.

        :param ctrl: The control qubit used to control the Hamiltonian gate.
        :param targets: 2 qubits used to apply the Hamiltonian.
        :param params: floating point parameters.
        :param circuit: The associated quantum circuit.
        """

        if params is None:
            # Default parameters for a simple Hamiltonian (no powers)
            params = [0.19634953, 0.37900987, 0.9817477, 1.87900984, 0.58904862]

        used_qubits = [ctrl, targets[0], targets[1]]

        super().__init__(self.__class__.__name__,  # name
                         [],  # parameters
                         used_qubits,  # qubits
                         circuit)  # circuit

        self.comment("[HS] Start.")
        self.ccz(ctrl, targets[0], targets[1])
        self.crx(params[0], ctrl, targets[1])
        self._attach(csqtrx.CsqrtX(ctrl, targets[1], self).inverse())
        self.crzz(params[1], ctrl, targets[1])
        self.crx(params[2], ctrl, targets[0])
        self.crzz(params[3], ctrl, targets[0])
        self.ccx(ctrl, targets[0], targets[1])
        self.crx(params[4], ctrl, targets[0])
        self.ccx(ctrl, targets[0], targets[1])
        self.ccz(ctrl, targets[0], targets[1])
        self.comment("[HS] End.")


# Adding the method to the QuantumCircuit and CompositeGate classes.
def hamiltonian4x4(self, ctrl: QubitType, targets: Tuple[QubitType],
                   params: List[float] = None) -> Hamiltonian4x4Gate:
    self._check_qubit(ctrl)
    self._check_qubit(targets[0])
    self._check_qubit(targets[1])
    self._check_dups([ctrl, targets[0], targets[1]])
    return self._attach(Hamiltonian4x4Gate(ctrl, targets, params, self))


QuantumCircuit.hamiltonian4x4 = hamiltonian4x4
CompositeGate.hamiltonian4x4 = hamiltonian4x4
