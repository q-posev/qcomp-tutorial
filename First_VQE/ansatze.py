import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from excitations import *

def HF_initial_state(qubits):
    circuit = QuantumCircuit(qubits)
    for i in range(qubits//2, qubits):
        circuit.x(i)
    
    return circuit  

def UCCSD_ansatz(qubits, initial_state, excitations, angle):
    circuit = QuantumCircuit(qubits)

    circuit.append(initial_state, range(qubits))

    for exci in excitations:
        for key, term in exci.terms.items():
            if (len(key) % 2) == 0:
                if term <= 0:
                    circuit.append(double_excitation(key, -(1/8)*angle), range(qubits))
                else:
                    circuit.append(double_excitation(key, (1/8)*angle), range(qubits))
            else:
                if term <= 0:
                    circuit.append(single_excitation(key, angle), range(qubits))
                else:
                    circuit.append(single_excitation(key, angle), range(qubits))

    return circuit

def H2_UCCSD_ansatz_bis(qubits, initial_state, excitations, angle):
    circuit = QuantumCircuit(qubits)

    circuit.append(initial_state, range(qubits))

    circuit.append(single_excitation_bis((0,2), (1/2)*angle), range(qubits))
    circuit.append(single_excitation_bis((1,3), (1/2)*angle), range(qubits))
    circuit.append(double_excitation_bis(excitations, (1/8)*angle), range(qubits))

    return circuit
