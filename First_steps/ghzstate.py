import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_state_qsphere
from qiskit.quantum_info import Statevector

GHZ = QuantumCircuit(3)

GHZ.h(0)
GHZ.cnot(0,1)
GHZ.cnot(1,2)

GHZ_state = Statevector(GHZ)

print(GHZ)
print(GHZ_state)

GHZ_generalized = QuantumCircuit(8)
GHZ_generalized.h(0)
for i in range(7):
    GHZ_generalized.cnot(i,i+1)

GHZ_generalized_state = Statevector(GHZ_generalized)

print(GHZ_generalized)
plot_state_qsphere(GHZ_generalized_state, filename='training2.png')