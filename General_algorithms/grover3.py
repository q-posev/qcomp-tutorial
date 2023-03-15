import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile, assemble, Aer
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from math import sqrt, pi
from cmath import exp
from Grover import grover_algo

##Test with the example of 3 qubits and search of the states |101> and |110>
n = 3
qc = QuantumCircuit(n)
qc = grover_algo(qc, n)

print(qc)
qc.draw('mpl', filename='grover3qu_circ.png')

#Simulate this 3 qubits Grover algorithm
sim = Aer.get_backend('aer_simulator')
grover_circuit = transpile(qc, sim)
qobj = assemble(grover_circuit)
results = sim.run(qobj).result()
counts = results.get_counts()

plot_histogram(counts, filename='grover3qu_sim.png')