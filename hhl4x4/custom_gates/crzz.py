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

"""This module contains functions to apply a controlled-RZZ gate.

The Rzz gate is a phase shift gate:
$R_{zz} = \begin{pmatrix}e^{i\theta} & 0\\0 & e^{i\theta}\end{pmatrix}$
"""
from typing import Tuple
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
import hhl4x4.custom_gates.comment

QubitType = Tuple[QuantumRegister, int]


class CRZZGate(CompositeGate):

    def __init__(self, theta: float, ctrl: QubitType, target: QubitType,
                 circuit: QuantumCircuit = None):
        """Initialize the CRzzGate class.

        :param theta: Phase added to the quantum state of qubit.
        :param ctrl: The control qubit used to control the RZZ gate.
        :param target: The qubit on which the RZZ gate is applied.
        :param circuit: The associated quantum circuit.
        """
        used_qubits = [ctrl, target]

        super().__init__(self.__class__.__name__,  # name
                         [theta],  # parameters
                         used_qubits,  # qubits
                         circuit)  # circuit

        self.comment("c-RZZ")
        self.cu1(theta, ctrl, target)
        self.cx(ctrl, target)
        self.cu1(theta, ctrl, target)
        self.cx(ctrl, target)


def crzz(self, theta: float, ctrl: QubitType, target: QubitType) -> CRZZGate:
    self._check_qubit(ctrl)
    self._check_qubit(target)
    self._check_dups([ctrl, target])
    return self._attach(CRZZGate(theta, ctrl, target, self))


QuantumCircuit.crzz = crzz
CompositeGate.crzz = crzz
