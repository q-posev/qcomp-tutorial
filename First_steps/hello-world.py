import numpy as np
from qiskit import QuantumCircuit, Aer

sim = Aer.get_backend('aer_simulator')

phi_plus = QuantumCircuit(2)
phi_plus.h(0)
phi_plus.cnot(0,1)

phi_moins = QuantumCircuit(2)
phi_moins.h(0)
phi_moins.z(0)
phi_moins.cnot(0,1)

psi_plus = QuantumCircuit(2)
psi_plus.h(0)
psi_plus.x(1)
psi_plus.cnot(0,1)

psi_moins = QuantumCircuit(2)
psi_moins.h(0)
psi_moins.x(1)
psi_moins.z(0)
psi_moins.cnot(0,1)

from qiskit.quantum_info import Statevector

phi_plus_vec = Statevector(phi_plus)
print(phi_plus)
print(phi_plus_vec)

phi_moins_vec = Statevector(phi_moins)
print(phi_moins)
print(phi_moins_vec)

psi_plus_vec = Statevector(psi_plus)
print(psi_plus)
print(psi_plus_vec)

psi_moins_vec = Statevector(psi_moins)
print(psi_moins)
print(psi_moins_vec)