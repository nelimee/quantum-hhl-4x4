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

"""Implementation of a comment instruction.

The comment instruction is a hack to be able to insert comments in the
generated OpenQASM code. Comments are then ignored and removed by the
Qiskit compiler so they will only appear in the generated OpenQASM.

The Comment gate overloads the Barrier gate, which *does not* change the
circuit result but *might change* the final OpenQASM code by preventing
some optimisations.
"""

import qiskit
from qiskit.extensions.standard.barrier import Barrier


class Comment(Barrier):
    """Instruction inserting a comment in the OpenQASM code."""

    def __init__(self, text: str, qubits, circ):
        """Create new comment."""
        super().__init__(qubits, circ)
        self._text = text

    def inverse(self):
        """Do nothing. Return self."""
        return self

    def qasm(self):
        """Return OpenQASM string."""
        return "// {}".format(self._text)

    def reapply(self, circ):
        """Reapply this comment."""
        self._modifiers(circ.comment(self._text))

    def q_if(self, *qregs):
        self._text = ("c-" * len(qregs)) + self._text
        return self


def comment(self, text: str):
    """Write a comment to circuit."""
    all_qubits = []
    circuit = self
    while not hasattr(circuit, 'regs'):
        circuit = circuit.circuit
    for _, register in circuit.regs.items():
        if isinstance(register, qiskit.QuantumRegister):
           all_qubits.extend((register[i] for i in range(len(register))))
    return self._attach(Comment(text, all_qubits, self))


qiskit.QuantumCircuit.comment = comment
qiskit.CompositeGate.comment = comment
