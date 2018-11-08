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

"""This module contains all the functions and classes related to registers."""

import typing
from copy import deepcopy
import qiskit


def _get_slice_size(slice_instance: slice, container_size: int):
    start, stop, step = slice_instance.indices(container_size)
    return (stop - start) // step + (1 if (stop - start) % step != 0 else 0)


class QRegisterBase(qiskit.QuantumRegister):

    def __init__(self, *args, **kwargs):
        # Copy constructor
        if len(args) == 1 and isinstance(args[0], qiskit.QuantumRegister):
            quantum_register = args[0]
            super().__init__(quantum_register.size, quantum_register.name)
            if isinstance(args[0], QRegisterBase):
                self._reversed = quantum_register._reversed
            else:
                self._reversed = False
            self._register = args[0]

        elif len(args) >= 2 and isinstance(args[0], int) and isinstance(args[1],
                                                                        str):
            super().__init__(args[0], args[1])
            self._reversed = False
            self._register = self

        else:
            raise NotImplementedError("({})".format(','.join(map(type, args))))

    def _reverse_access_endian(self):
        """Reverse the apparent endianness of the register.
        This operation does not produce any gate in the quantum circuit because
        the endianness is just reversed when accessing to a specific qubit.
        """
        # Update the flag
        self._reversed = not self._reversed

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SplittableQuantumRegister(self._register, key)
        else:
            if self._reversed:
                return self._register.__getitem__(len(self._register) - 1 - key)
            else:
                return self._register.__getitem__(key)

    def __add__(self, other):
        return BondableQuantumRegister(self._register, other)

    def __iadd__(self, other):
        return BondableQuantumRegister(self._register, other)


class SplittableQuantumRegister(QRegisterBase):
    """Implement a splittable register.
    A splittable register is an instance of QuantumRegister that can be indexed
    with Python slices. The SplittableQuantumRegister class implement the
    operations:
        1) Creation from an instance of QuantumRegister, with an additional
           optional third parameter corresponding to the slice to use.
        2) Use of classical indices and of slices:
               splittable_reg = SplittableQuantumRegister("qreg", 10)
               qubit_3 = splittable_reg[3]
               qubit_6 = splittable_reg[::3][2]
    """

    def __init__(self, qreg: QRegisterBase, *args):
        if len(args) >= 1 and isinstance(args[0], slice):
            self._slice = args[0]
            # Update the size if the slice is given by the user
            size = _get_slice_size(self._slice, len(qreg))
        else:
            self._slice = slice(len(qreg))
            size = len(qreg)
        super().__init__(qreg)
        self.size = size
        # Deepcopy is terrible if we chain a huge amount of slicings
        # but it avoids side effects.
        self._register = deepcopy(qreg)

    def __getitem__(self, key: typing.Union[int, slice]):
        # If the user gave a slice, then return an other splittable register.
        if isinstance(key, slice):
            return SplittableQuantumRegister(self, key)
        # Else, recursively call __getitem__ on the self._register list.
        else:
            start, stop, step = self._slice.indices(self.size)
            if key < 0 or key >= stop:
                raise IndexError(
                    ("Trying to obtain the bit n°{} from a register of size {"
                     "}").format(key, self.size))
            if self._reversed:
                return self._register.__getitem__(
                    start + (self.size - 1 - key) * step)
            else:
                return self._register.__getitem__(start + key * step)

    def __add__(self, other: QRegisterBase):
        return BondableQuantumRegister(self, other)

    def __iadd__(self, other: QRegisterBase):
        return self + other


class BondableQuantumRegister(QRegisterBase):
    """Implement a bondable register.
    A bondable register is an instance of QuantumRegister that can be
    composed of
    one or more QuantumRegister that are glued together.
    The class BondableQuantumRegister implements the operations:
    """

    def __init__(self, qreg: QRegisterBase, *args):
        # Construct from a list of QuantumRegisters
        # Deepcopy is terrible if we chain a huge amount of bonding
        # but it avoids side effects.
        self._registers = [deepcopy(qreg)]
        self._registers += [deepcopy(arg) for arg in args if
                            isinstance(arg, QRegisterBase)]
        # Concatenating the names and summing the sizes.
        super().__init__("".join(map(lambda x: x.name, self._registers)),
                         sum(map(lambda x: x.size, self._registers)))

    def __getitem__(self, key: int):
        if isinstance(key, slice):
            return SplittableQuantumRegister(self, key)

        total_index = 0
        registers = self._registers if not self._reversed else self._registers[
                                                               ::-1]
        for register in registers:
            if (key - total_index) < len(register):
                if self._reversed:
                    return register[len(register) - 1 - (key - total_index)]
                else:
                    return register[key - total_index]
            total_index += len(register)
        # If we are here, this means that the given key was not a valid index
        # for the register, so we raise an exception
        raise IndexError(
            "Trying to obtain the bit n°{} from a register of size {}".format(
                key, self.size))

    def __add__(self, other: QRegisterBase):
        return BondableQuantumRegister(self, other)

    def __iadd__(self, other: QRegisterBase):
        return self + other


class CRegisterBase(qiskit.ClassicalRegister):
    """Classical Register."""
    def __init__(self, *args, **kwargs):
        # Copy constructor
        if len(args) == 1 and isinstance(args[0], qiskit.ClassicalRegister):
            classical_register = args[0]
            self.name = classical_register.name
            self.size = classical_register.size
        # Delegate the constructor to the super class.
        else:
            super().__init__(*args, **kwargs)
