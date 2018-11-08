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

"""This module define some useful functions and types to deal with endianness.
"""

import typing
import qiskit

from .registers import QRegisterBase, CRegisterBase

# Type alias definition
GateContainer = typing.Union[qiskit.QuantumCircuit, qiskit.CompositeGate]

class QRegisterLE(QRegisterBase):
    """Quantum Register Little Endian."""
    pass

class QRegisterBE(QRegisterBase):
    """Quantum Register Big Endian."""
    pass

class QRegisterPhaseLE(QRegisterBase):
    """Quantum Register Little Endian in Quantum Fourier Transform state."""
    pass

class QRegisterPhaseBE(QRegisterBase):
    """Quantum Register Big Endian in Quantum Fourier Transform state."""
    pass


class CRegister(CRegisterBase):
    """Classical Register."""
    pass


def apply_LE_operation(container: GateContainer,
                       little_endian_operation,
                       qreg: qiskit.QuantumRegister):
    """Apply a little endian operation to a quantum register.
    This function will change the endianness of the given register if
    it is not already in little endian, apply the operation, and recover
    the initial endianness.
    Warning: if the type of the given register does not give any
             information on its endianness (inheriting from
             QRegisterLE or QRegisterBE) then the operation will be
             applied on the register without any endianness
             consideration.
    """

    if isinstance(qreg, QRegisterBE):
        qreg._reverse_access_endian()

    # Here we may have an instance of QRegisterBE which is
    # in little endian when we access it. This should be
    # avoided, that is why the method _reverse_access_endian
    # is "private".

    little_endian_operation(container, qreg)

    # As written above, we may have a strange register (labeled
    # as big endian but effectively in little endian). Don't
    # forget to fix this register by changing again it's
    # endianness.

    if isinstance(qreg, QRegisterBE):
        qreg._reverse_access_endian()

def apply_BE_operation(container: GateContainer,
                       big_endian_operation,
                       qreg: qiskit.QuantumRegister):
    """Apply a big endian operation to a quantum register.
    This function will change the endianness of the given register if
    it is not already in big endian, apply the operation, and recover
    the initial endianness.
    Warning: if the type of the given register does not give any
             information on its endianness (inheriting from
             QRegisterLE or QRegisterBE) then the operation will be
             applied on the register without any endianness
             consideration.
    """

    if isinstance(qreg, QRegisterLE):
        qreg._reverse_access_endian()

    # Here we may have an instance of QRegisterLE which is
    # in big endian when we access it. This should be
    # avoided, that is why the method _reverse_access_endian
    # is "private".

    big_endian_operation(container, qreg)

    # As written above, we may have a strange register (labeled
    # as little endian but effectively in big endian). Don't
    # forget to fix this register by changing again it's
    # endianness.

    if isinstance(qreg, QRegisterLE):
        qreg._reverse_access_endian()


def swap_endianness(self: GateContainer,
                    qreg: typing.Union[QRegisterBE, QRegisterLE]):
    """Swaps the endianness of qreg."""
    qubit_number = len(qreg)
    for i in range(qubit_number//2):
        self.swap(qreg[i], qreg[qubit_number-1-i])


