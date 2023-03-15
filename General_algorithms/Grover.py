import numpy as np
from qiskit import QuantumCircuit, transpile, assemble, Aer
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_qsphere
from qiskit.quantum_info import Statevector
from math import sqrt, pi
from cmath import exp

#Initialize the circuits in the states |++...+>
def initialize_s(circuit, qubits):
    for q in range(qubits):
        circuit.h(q)
    return circuit

#Diffuser of the Grover's algorithm
def diffuser_grover(qubits):
    circuit = QuantumCircuit(qubits)
    for qubit in range(qubits):
        circuit.h(qubit)
    for qubit in range(qubits):
        circuit.x(qubit)
    circuit.h(qubits-1)
    circuit.mct(list(range(qubits-1)), qubits-1)
    circuit.h(qubits-1)
    for qubit in range(qubits):
        circuit.x(qubit)
    for qubit in range(qubits):
        circuit.h(qubit)
    
    U_s = circuit.to_gate()
    U_s.name = "U$_s$"
    circuit.barrier()
    return U_s

#Grover's oracle that marks the wanted states
# two wanted states (|101> and |110> for the 3 qubits case here)
def oracle_grover(qubits):
    circuit = QuantumCircuit(qubits)
#The part of the Grover's oracle that is marking the wanted states is the one below, encapsulating between hastags. In all generality, it consists on applying
#specific (multi)-controlled-Z gates that will flip the coefficients of the wanted states from positive to negative value. Here we are giving a special case
#of Grover's oracle which marks specific states and that is in particular the correct oracle for the example shown in grover3qubit.py
##################################################################################
    for q in range(qubits-1):
        circuit.cz(q, qubits-1)
##################################################################################
    oracle_nqubits = circuit.to_gate()
    oracle_nqubits.name = "U$_\omega$"
    return oracle_nqubits

#Function that performs the Grover's algorithm
def grover_algo(circuit, qubits):
    circuit = initialize_s(circuit, qubits)
    circuit.append(oracle_grover(qubits), range(qubits))
    circuit.append(diffuser_grover(qubits), range(qubits))
    circuit.measure_all()
    return circuit

oracle = QuantumCircuit(3)
oracle.append(oracle_grover(3), range(3))

diffuser = QuantumCircuit(3)
diffuser.append(diffuser_grover(3), range(3))

oracle.decompose().draw('mpl', filename='grover_oracle.png')
diffuser.decompose().draw('mpl', filename='grover_diffuser.png')