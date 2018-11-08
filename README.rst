
This repository contains an implementation of the HHL algorithm for a specific
4 x 4 matrix:

.. code::python

    A = 1/4 * numpy.array([[15, 9, 5, -3],
                           [9, 15, 3, -5],
                           [5, 3, 15, -9],
                           [-3, -5, -9, 15]])

The implementation is inspired from the paper `Quantum Circuit Design for
Solving Linear Systems of Equations`_, written by Yudong Cao, Anmer
Daskin, Steven Frankel and Sabre Kais.

.. _Quantum Circuit Design for Solving Linear Systems of Equations: https://arxiv.org/abs/1110.2232v2

Installation
============

The installation procedure is composed of multiple steps, some of them being optional:

1) (optional) Create a virtual environment to isolate the installation:

.. code:: shell

    python3 -m venv hhl_venv
    source hhl_venv/bin/activate

2) Clone the git repository:

.. code:: shell

   git clone https://github.com/nelimee/quantum-hhl-4x4.git
   cd quantum-hhl-4x4

3) Install the requirements:

 .. code:: shell

    pip install -r requirements.txt

4) Install the HHL implementation:

.. code:: shell

   python3 setup.py install


Description of the repository structure
=======================================

The main directory contains:

1) A ``LICENSE`` file explaining under which license this code is distributed.
   For more information go read the `Notes about the license`_ section.
2) This README file.
3) A ``requirements.txt`` file that can be used to install all the dependencies
   of the software.
4) A ``setup.py`` file used to install the code.
5) The ``hhl4x4`` directory which contains all the Python code.

The ``hhl4x4`` folder
---------------------

The ``hhl4x4`` folder contains all the Python code used to implement the HHL algorithm
for the matrix :math:`A`. It is organised in 2 folders and 3 python files:

1) The ``custom_gates`` folder contains the implementation of user-defined quantum gates
   like the doubly-controlled ``Z`` gate (a ``Z`` gate controlled by 2 qubits) or the
   controlled Rzz gate (a controlled global phase shift).
   The HHL algorithm is implemented a user-defined quantum gate in the file ``hhl4x4.py``.
2) The ``utils`` folder contains 2 python files: ``endianness.py`` used to take care of
   the registers endianness and ``registers.py`` that implements wrapper around the base
   register classes used by Qiskit.
3) ``4x4.py``: the full implementation of the HHL algorithm. Once the software is installed
   (after a successful ``python setup.py install``) you can run this file by typing the
   command ``HHL4x4`` in your terminal.
4) ``optimise_parameters.py``: the script used to find the best parameters for the Hamiltonian
   simulation part. Once the software is installed (after a successful ``python setup.py install``)
   you can run this file by typing the command ``HHL4x4_optimise_parameters`` in your terminal.
   You can see the available options with ``HHL4x4_optimise_parameters --help``.

Note: The ``HHL4x4`` command or the `4x4.py` script will generate the file ``4x4.qasm`` containing
the OpenQASM code of the implemented HHL algorithm in the current directory. A histogram visualisation
of the final quantum state will also pop at the end of the program.


Notes about the license
=======================

This software is licensed under the CeCILL-B license. The CeCILL-B license enforce the
obligation for anyone who want to use this software (in any way) to cite the original authors
and source.

If you want to use this software, please cite:

1) Adrien Suau, adrien.suau@cerfacs.fr as the main author.
2) CERFACS, cerfacs.fr as a contributor.

If you have any doubt, please read the license. If you still have doubts or questions, please
send me a mail at adrien.suau@cerfacs.fr.
