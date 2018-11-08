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

"""This module contains an implementation of the Quantum Fourier Transform.
For the moment the implementation is the most simple quantum fourier transform
implementation. It has a gate complexity of O(n²). The algorithm implemented is
the one presented on the wikipedia page of QFT:
https://en.wikipedia.org/wiki/Quantum_Fourier_transform
"""

import math

import sympy as sym
from qiskit import QuantumCircuit, QuantumRegister, CompositeGate
from hhl4x4.utils.endianness import QRegisterBE, \
    QRegisterBase, \
    apply_BE_operation


class ApproximateQFTGate(CompositeGate):
    """Approximation of the QFT gate on quantum register.

    This implementation follows the one described in the Wikipedia page of the
    Quantum Fourier Transform:
    https://en.wikipedia.org/wiki/Quantum_Fourier_transform
    #Circuit_implementation
    This algorithm is also the one choosen by Microsoft in their
    Microsoft.Quantum.Canon.
    Warning: This gate does not swap the endianness of the output to return a
    register with the same endianness as the given one. The endianness of qreg
    is reversed by the quantum fourier transform algorithm, and so a big-endian
    register will become little-endian, even if its type does not say so.
    """

    def __init__(self, qreg: QuantumRegister, qcirc: QuantumCircuit,
                 approximation: int = None):
        """Initialise an ApproximateQFTGate.

        :param qreg: The quantum register on which to apply the approximate
        quantum Fourier transform.
        :param qcirc: The associated QuantumCircuit.
        :param approximation: The order of approximation. All the controlled
        phase gates with an angle inferior to pi/2**approximation will not be
        added to the circuit. If not present, takes the best approximation
        possible. For more details see https://arxiv.org/abs/quant-ph/9601018.
        """

        qubits_number = len(qreg)
        used_qubits = [qreg[i] for i in range(qubits_number)]
        # If approximation is not set to a specific value, we choose a value
        # which is near to the optimum.
        # See https://arxiv.org/pdf/quant-ph/9601018.pdf
        if not approximation:
            approximation = math.ceil(math.log2(qubits_number)) + 2

        super().__init__(self.__class__.__name__,  # name
                         [approximation],  # parameters
                         used_qubits,  # qubits
                         qcirc)  # circuit

        for i in range(qubits_number):
            for j in range(max(0, i - approximation + 1), i):
                self.cu1(sym.pi / 2 ** (i - j), qreg[i], qreg[j])
            self.h(qreg[i])


def approximate_qft_be(self, qreg: QRegisterBE, qcirc: QuantumCircuit,
                       approximation: int = None) -> ApproximateQFTGate:
    """Add an ApproximateQFTGate."""
    self._check_qreg(qreg)
    gate = self._attach(ApproximateQFTGate(qreg, qcirc, approximation))
    # Here the QFT algorithm reversed the endianness, so as we don't want some
    # register with a strange behaviour (registers of type QRegisterBE that are
    # in little-endian for example), we reverse the endianness.
    qreg._reverse_access_endian()
    return gate


def iapproximate_qft_be(self, qreg: QRegisterBE, qcirc: QuantumCircuit,
                        approximation: int = None) -> ApproximateQFTGate:
    """Add an inverted ApproximateQFTGate."""
    self._check_qreg(qreg)
    # The QFT algorithm reverse the endianness, so the inverse QFT algorithm
    # also
    # and as it is the inverse algorithm, the endianness swap should occurs
    # before
    # the inverse QFT algorithm.
    qreg._reverse_access_endian()
    return self._attach(
        ApproximateQFTGate(qreg, qcirc, approximation).inverse())


class QFTGate(ApproximateQFTGate):
    """Exact QFT gate on quantum register.

    Implementation use the ApproximateQFTGate with an approximation order large
    enough to change the approximation in an exact computation.
    Warning: This gate does not swap the endianness of the output to return a
    register with the same endianness as the one given. The endianness of qreg
    is reversed by the quantum fourier transform algorithm, and so a big-endian
    register will become little-endian, even if its type does not say so.
    """

    def __init__(self, qreg: QuantumRegister, qcirc: QuantumCircuit):
        super().__init__(qreg, qcirc, approximation=len(qreg))


def qft_be(self, qreg: QRegisterBE, qcirc: QuantumCircuit) -> QFTGate:
    """Add a QFTGate."""
    self._check_qreg(qreg)
    gate = self._attach(QFTGate(qreg, qcirc))
    # Here the QFT algorithm reversed the endianness, so as we don't want some
    # register with a strange behaviour (registers of type QRegisterBE that are
    # in little-endian for example), we reverse the endianness.
    qreg._reverse_access_endian()
    return gate


def iqft_be(self, qreg: QRegisterBE, qcirc: QuantumCircuit) -> QFTGate:
    """Add an inverted QFTBEGate."""
    self._check_qreg(qreg)
    # The QFT algorithm reverse the endianness, so the inverse QFT algorithm
    # also
    # and as it is the inverse algorithm, the endianness swap should occurs
    # before
    # the inverse QFT algorithm.
    qreg._reverse_access_endian()
    return self._attach(QFTGate(qreg, qcirc).inverse())


def apply_in_fourier_basis(self, operation, qreg: QRegisterBase,
                           qcirc: QuantumCircuit, **kwargs):
    """Apply the given operation in the Fourier basis."""

    # Defining first our big endian operation.
    def big_endian_operation(self_local, qreg_local):
        # Here, 'self' and 'qreg' refer to the local parameters,
        # 'qcirc' and 'kwargs' refer to the parameters of the parent scope.
        qft_be(self_local, qreg_local, qcirc)
        operation(self_local, qreg_local, **kwargs)
        iqft_be(self_local, qreg_local, qcirc)

    apply_BE_operation(self, big_endian_operation, qreg)


def apply_in_approx_fourier_basis(self, operation, qreg: QRegisterBase,
                                  qcirc: QuantumCircuit,
                                  approximation: int = None, **kwargs):
    """Apply the given operation in the approximate Fourier basis."""

    # Defining first our big endian operation.
    def big_endian_operation(self_local, qreg_local):
        # Here, 'self' and 'qreg' refer to the local parameters,
        # 'qcirc', 'kwargs' and 'approximation' refer to the parameters
        # of the parent scope.
        approximate_qft_be(self, qreg, qcirc, approximation)
        operation(self, qreg, **kwargs)
        iapproximate_qft_be(self, qreg, qcirc, approximation)

    apply_BE_operation(self, big_endian_operation, qreg)
