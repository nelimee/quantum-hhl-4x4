OPENQASM 2.0;
include "qelib1.inc";
qreg q0[1];
qreg q1[4];
qreg q2[2];
creg c0[1];
// [4x4] Initialising b.
h q2[0];
h q2[1];
// [4x4] Initialisation done!
// [4x4] 1. Quantum phase estimation.
// [QPE] Starting block.
// [QPE] 1. Hadamard gate.
h q1[0];
h q1[1];
h q1[2];
h q1[3];
// [QPE] 2. Phase estimation.
// [QPE] 2.0. Start of step 0 of phase estimation.
// [HS] Start.
// CCZ
h q2[1];
ccx q1[3],q2[0],q2[1];
h q2[1];
// c-RX
cu3(0.196349530000000,pi/2,3*pi/2) q1[3],q2[1];
// c-RZZ
cu1(pi) q1[3],q2[1];
cx q1[3],q2[1];
cu1(pi) q1[3],q2[1];
cx q1[3],q2[1];
h q2[1];
t q2[1];
cx q1[3],q2[1];
t q1[3];
tdg q2[1];
h q2[1];
cz q1[3],q2[1];
cx q1[3],q2[1];
// c-sqrt(X)
// c-RZZ
cu1(0.379009870000000) q1[3],q2[1];
cx q1[3],q2[1];
cu1(0.379009870000000) q1[3],q2[1];
cx q1[3],q2[1];
// c-RX
cu3(0.981747700000000,pi/2,3*pi/2) q1[3],q2[0];
// c-RZZ
cu1(pi) q1[3],q2[0];
cx q1[3],q2[0];
cu1(pi) q1[3],q2[0];
cx q1[3],q2[0];
// c-RZZ
cu1(1.87900984000000) q1[3],q2[0];
cx q1[3],q2[0];
cu1(1.87900984000000) q1[3],q2[0];
cx q1[3],q2[0];
ccx q1[3],q2[0],q2[1];
// c-RX
cu3(0.589048620000000,pi/2,3*pi/2) q1[3],q2[0];
// c-RZZ
cu1(pi) q1[3],q2[0];
cx q1[3],q2[0];
cu1(pi) q1[3],q2[0];
cx q1[3],q2[0];
ccx q1[3],q2[0],q2[1];
// CCZ
h q2[1];
ccx q1[3],q2[0],q2[1];
h q2[1];
// [HS] End.
// [QPE] 2.0. End of step 0 of phase estimation.
// [QPE] 2.1. Start of step 1 of phase estimation.
// [HS] Start.
// CCZ
h q2[1];
ccx q1[2],q2[0],q2[1];
h q2[1];
// c-RX
cu3(1.96349540000000,pi/2,3*pi/2) q1[2],q2[1];
// c-RZZ
cu1(pi) q1[2],q2[1];
cx q1[2],q2[1];
cu1(pi) q1[2],q2[1];
cx q1[2],q2[1];
h q2[1];
t q2[1];
cx q1[2],q2[1];
t q1[2];
tdg q2[1];
h q2[1];
cz q1[2],q2[1];
cx q1[2],q2[1];
// c-sqrt(X)
// c-RZZ
cu1(1.11532058000000) q1[2],q2[1];
cx q1[2],q2[1];
cu1(1.11532058000000) q1[2],q2[1];
cx q1[2],q2[1];
// c-RX
cu3(1.96349540000000,pi/2,3*pi/2) q1[2],q2[0];
// c-RZZ
cu1(pi) q1[2],q2[0];
cx q1[2],q2[0];
cu1(pi) q1[2],q2[0];
cx q1[2],q2[0];
// c-RZZ
cu1(2.61532069000000) q1[2],q2[0];
cx q1[2],q2[0];
cu1(2.61532069000000) q1[2],q2[0];
cx q1[2],q2[0];
ccx q1[2],q2[0],q2[1];
// c-RX
cu3(1.17809726000000,pi/2,3*pi/2) q1[2],q2[0];
// c-RZZ
cu1(pi) q1[2],q2[0];
cx q1[2],q2[0];
cu1(pi) q1[2],q2[0];
cx q1[2],q2[0];
ccx q1[2],q2[0],q2[1];
// CCZ
h q2[1];
ccx q1[2],q2[0],q2[1];
h q2[1];
// [HS] End.
// [QPE] 2.1. End of step 1 of phase estimation.
// [QPE] 2.2. Start of step 2 of phase estimation.
// [HS] Start.
// CCZ
h q2[1];
ccx q1[1],q2[0],q2[1];
h q2[1];
// c-RX
cu3(-0.785398160000000,pi/2,3*pi/2) q1[1],q2[1];
// c-RZZ
cu1(pi) q1[1],q2[1];
cx q1[1],q2[1];
cu1(pi) q1[1],q2[1];
cx q1[1],q2[1];
h q2[1];
t q2[1];
cx q1[1],q2[1];
t q1[1];
tdg q2[1];
h q2[1];
cz q1[1],q2[1];
cx q1[1],q2[1];
// c-sqrt(X)
// c-RZZ
cu1(1.01714584000000) q1[1],q2[1];
cx q1[1],q2[1];
cu1(1.01714584000000) q1[1],q2[1];
cx q1[1],q2[1];
// c-RX
cu3(3.92699082000000,pi/2,3*pi/2) q1[1],q2[0];
// c-RZZ
cu1(pi) q1[1],q2[0];
cx q1[1],q2[0];
cu1(pi) q1[1],q2[0];
cx q1[1],q2[0];
// c-RZZ
cu1(2.51714589000000) q1[1],q2[0];
cx q1[1],q2[0];
cu1(2.51714589000000) q1[1],q2[0];
cx q1[1],q2[0];
ccx q1[1],q2[0],q2[1];
// c-RX
cu3(2.35619449000000,pi/2,3*pi/2) q1[1],q2[0];
// c-RZZ
cu1(pi) q1[1],q2[0];
cx q1[1],q2[0];
cu1(pi) q1[1],q2[0];
cx q1[1],q2[0];
ccx q1[1],q2[0],q2[1];
// CCZ
h q2[1];
ccx q1[1],q2[0],q2[1];
h q2[1];
// [HS] End.
// [QPE] 2.2. End of step 2 of phase estimation.
// [QPE] 2.3. Start of step 3 of phase estimation.
// [HS] Start.
// CCZ
h q2[1];
ccx q1[0],q2[0],q2[1];
h q2[1];
// c-RX
cu3(-9.01416169000000e-9,pi/2,3*pi/2) q1[0],q2[1];
// c-RZZ
cu1(pi) q1[0],q2[1];
cx q1[0],q2[1];
cu1(pi) q1[0],q2[1];
cx q1[0],q2[1];
h q2[1];
t q2[1];
cx q1[0],q2[1];
t q1[0];
tdg q2[1];
h q2[1];
cz q1[0],q2[1];
cx q1[0],q2[1];
// c-sqrt(X)
// c-RZZ
cu1(-0.750000046000000) q1[0],q2[1];
cx q1[0],q2[1];
cu1(-0.750000046000000) q1[0],q2[1];
cx q1[0],q2[1];
// c-RX
cu3(1.57079632000000,pi/2,3*pi/2) q1[0],q2[0];
// c-RZZ
cu1(pi) q1[0],q2[0];
cx q1[0],q2[0];
cu1(pi) q1[0],q2[0];
cx q1[0],q2[0];
// c-RZZ
cu1(0.750000039000000) q1[0],q2[0];
cx q1[0],q2[0];
cu1(0.750000039000000) q1[0],q2[0];
cx q1[0],q2[0];
ccx q1[0],q2[0],q2[1];
// c-RX
cu3(-1.57079633000000,pi/2,3*pi/2) q1[0],q2[0];
// c-RZZ
cu1(pi) q1[0],q2[0];
cx q1[0],q2[0];
cu1(pi) q1[0],q2[0];
cx q1[0],q2[0];
ccx q1[0],q2[0],q2[1];
// CCZ
h q2[1];
ccx q1[0],q2[0],q2[1];
h q2[1];
// [HS] End.
// [QPE] 2.3. End of step 3 of phase estimation.
// [QPE] 3. Inverse QFT.
h q1[0];
cu1(-pi/2) q1[0],q1[1];
cu1(-pi/4) q1[0],q1[2];
cu1(-pi/8) q1[0],q1[3];
h q1[1];
cu1(-pi/2) q1[1],q1[2];
cu1(-pi/4) q1[1],q1[3];
h q1[2];
cu1(-pi/2) q1[2],q1[3];
h q1[3];
// [QPE] End block.
// [4x4] Inverting computed eigenvalues.
swap q1[2],q1[1];
// [4x4] 2. Phase rotation.
// CRY
cu3(0.25*pi,0,0) q1[0],q0[0];
// CRY
cu3(0.125*pi,0,0) q1[1],q0[0];
// CRY
cu3(0.0625*pi,0,0) q1[2],q0[0];
// CRY
cu3(0.03125*pi,0,0) q1[3],q0[0];
// Inverting the inversion of eigenvalues.
swap q1[2],q1[1];
// [4x4] 3. Inverting quantum phase estimation.
// [QPE] End block.
h q1[3];
cu1(pi/2) q1[2],q1[3];
h q1[2];
cu1(pi/4) q1[1],q1[3];
cu1(pi/2) q1[1],q1[2];
h q1[1];
cu1(pi/8) q1[0],q1[3];
cu1(pi/4) q1[0],q1[2];
cu1(pi/2) q1[0],q1[1];
h q1[0];
// [QPE] 3. Inverse QFT.
// [QPE] 2.3. End of step 3 of phase estimation.
// [HS] End.
h q2[1];
ccx q1[0],q2[0],q2[1];
h q2[1];
// CCZ
ccx q1[0],q2[0],q2[1];
cx q1[0],q2[0];
cu1(-pi) q1[0],q2[0];
cx q1[0],q2[0];
cu1(-pi) q1[0],q2[0];
// c-RZZ
cu3(1.57079633000000,-3*pi/2,-pi/2) q1[0],q2[0];
// c-RX
ccx q1[0],q2[0],q2[1];
cx q1[0],q2[0];
cu1(-0.750000039000000) q1[0],q2[0];
cx q1[0],q2[0];
cu1(-0.750000039000000) q1[0],q2[0];
// c-RZZ
cx q1[0],q2[0];
cu1(-pi) q1[0],q2[0];
cx q1[0],q2[0];
cu1(-pi) q1[0],q2[0];
// c-RZZ
cu3(-1.57079632000000,-3*pi/2,-pi/2) q1[0],q2[0];
// c-RX
cx q1[0],q2[1];
cu1(0.750000046000000) q1[0],q2[1];
cx q1[0],q2[1];
cu1(0.750000046000000) q1[0],q2[1];
// c-RZZ
// c-sqrt(X)
cx q1[0],q2[1];
cz q1[0],q2[1];
h q2[1];
t q2[1];
tdg q1[0];
cx q1[0],q2[1];
tdg q2[1];
h q2[1];
cx q1[0],q2[1];
cu1(-pi) q1[0],q2[1];
cx q1[0],q2[1];
cu1(-pi) q1[0],q2[1];
// c-RZZ
cu3(9.01416169000000e-9,-3*pi/2,-pi/2) q1[0],q2[1];
// c-RX
h q2[1];
ccx q1[0],q2[0],q2[1];
h q2[1];
// CCZ
// [HS] Start.
// [QPE] 2.3. Start of step 3 of phase estimation.
// [QPE] 2.2. End of step 2 of phase estimation.
// [HS] End.
h q2[1];
ccx q1[1],q2[0],q2[1];
h q2[1];
// CCZ
ccx q1[1],q2[0],q2[1];
cx q1[1],q2[0];
cu1(-pi) q1[1],q2[0];
cx q1[1],q2[0];
cu1(-pi) q1[1],q2[0];
// c-RZZ
cu3(-2.35619449000000,-3*pi/2,-pi/2) q1[1],q2[0];
// c-RX
ccx q1[1],q2[0],q2[1];
cx q1[1],q2[0];
cu1(-2.51714589000000) q1[1],q2[0];
cx q1[1],q2[0];
cu1(-2.51714589000000) q1[1],q2[0];
// c-RZZ
cx q1[1],q2[0];
cu1(-pi) q1[1],q2[0];
cx q1[1],q2[0];
cu1(-pi) q1[1],q2[0];
// c-RZZ
cu3(-3.92699082000000,-3*pi/2,-pi/2) q1[1],q2[0];
// c-RX
cx q1[1],q2[1];
cu1(-1.01714584000000) q1[1],q2[1];
cx q1[1],q2[1];
cu1(-1.01714584000000) q1[1],q2[1];
// c-RZZ
// c-sqrt(X)
cx q1[1],q2[1];
cz q1[1],q2[1];
h q2[1];
t q2[1];
tdg q1[1];
cx q1[1],q2[1];
tdg q2[1];
h q2[1];
cx q1[1],q2[1];
cu1(-pi) q1[1],q2[1];
cx q1[1],q2[1];
cu1(-pi) q1[1],q2[1];
// c-RZZ
cu3(0.785398160000000,-3*pi/2,-pi/2) q1[1],q2[1];
// c-RX
h q2[1];
ccx q1[1],q2[0],q2[1];
h q2[1];
// CCZ
// [HS] Start.
// [QPE] 2.2. Start of step 2 of phase estimation.
// [QPE] 2.1. End of step 1 of phase estimation.
// [HS] End.
h q2[1];
ccx q1[2],q2[0],q2[1];
h q2[1];
// CCZ
ccx q1[2],q2[0],q2[1];
cx q1[2],q2[0];
cu1(-pi) q1[2],q2[0];
cx q1[2],q2[0];
cu1(-pi) q1[2],q2[0];
// c-RZZ
cu3(-1.17809726000000,-3*pi/2,-pi/2) q1[2],q2[0];
// c-RX
ccx q1[2],q2[0],q2[1];
cx q1[2],q2[0];
cu1(-2.61532069000000) q1[2],q2[0];
cx q1[2],q2[0];
cu1(-2.61532069000000) q1[2],q2[0];
// c-RZZ
cx q1[2],q2[0];
cu1(-pi) q1[2],q2[0];
cx q1[2],q2[0];
cu1(-pi) q1[2],q2[0];
// c-RZZ
cu3(-1.96349540000000,-3*pi/2,-pi/2) q1[2],q2[0];
// c-RX
cx q1[2],q2[1];
cu1(-1.11532058000000) q1[2],q2[1];
cx q1[2],q2[1];
cu1(-1.11532058000000) q1[2],q2[1];
// c-RZZ
// c-sqrt(X)
cx q1[2],q2[1];
cz q1[2],q2[1];
h q2[1];
t q2[1];
tdg q1[2];
cx q1[2],q2[1];
tdg q2[1];
h q2[1];
cx q1[2],q2[1];
cu1(-pi) q1[2],q2[1];
cx q1[2],q2[1];
cu1(-pi) q1[2],q2[1];
// c-RZZ
cu3(-1.96349540000000,-3*pi/2,-pi/2) q1[2],q2[1];
// c-RX
h q2[1];
ccx q1[2],q2[0],q2[1];
h q2[1];
// CCZ
// [HS] Start.
// [QPE] 2.1. Start of step 1 of phase estimation.
// [QPE] 2.0. End of step 0 of phase estimation.
// [HS] End.
h q2[1];
ccx q1[3],q2[0],q2[1];
h q2[1];
// CCZ
ccx q1[3],q2[0],q2[1];
cx q1[3],q2[0];
cu1(-pi) q1[3],q2[0];
cx q1[3],q2[0];
cu1(-pi) q1[3],q2[0];
// c-RZZ
cu3(-0.589048620000000,-3*pi/2,-pi/2) q1[3],q2[0];
// c-RX
ccx q1[3],q2[0],q2[1];
cx q1[3],q2[0];
cu1(-1.87900984000000) q1[3],q2[0];
cx q1[3],q2[0];
cu1(-1.87900984000000) q1[3],q2[0];
// c-RZZ
cx q1[3],q2[0];
cu1(-pi) q1[3],q2[0];
cx q1[3],q2[0];
cu1(-pi) q1[3],q2[0];
// c-RZZ
cu3(-0.981747700000000,-3*pi/2,-pi/2) q1[3],q2[0];
// c-RX
cx q1[3],q2[1];
cu1(-0.379009870000000) q1[3],q2[1];
cx q1[3],q2[1];
cu1(-0.379009870000000) q1[3],q2[1];
// c-RZZ
// c-sqrt(X)
cx q1[3],q2[1];
cz q1[3],q2[1];
h q2[1];
t q2[1];
tdg q1[3];
cx q1[3],q2[1];
tdg q2[1];
h q2[1];
cx q1[3],q2[1];
cu1(-pi) q1[3],q2[1];
cx q1[3],q2[1];
cu1(-pi) q1[3],q2[1];
// c-RZZ
cu3(-0.196349530000000,-3*pi/2,-pi/2) q1[3],q2[1];
// c-RX
h q2[1];
ccx q1[3],q2[0],q2[1];
h q2[1];
// CCZ
// [HS] Start.
// [QPE] 2.0. Start of step 0 of phase estimation.
// [QPE] 2. Phase estimation.
h q1[3];
h q1[2];
h q1[1];
h q1[0];
// [QPE] 1. Hadamard gate.
// [QPE] Starting block.
// [4x4] 4. Measurement.
measure q0[0] -> c0[0];
