import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def single_excitation(key, name_angle):

    if name_angle is None:
        theta = Parameter('theta')
    else:
        theta = Parameter(name_angle)

    num_qubits = key[1][0] - key[0][0] + 1
    length_key = len(key)

    circuit = QuantumCircuit(num_qubits)

    for i in range(length_key):
        if key[i][1] == 'X':
            circuit.h(key[i][0])
        elif key[i][1] == 'Y':
            circuit.rx(np.pi/2, key[i][0])
    
    for i in reversed(range(key[0][0], key[1][0])):
        circuit.cnot(i+1, i)

    circuit.rz(theta, 0)

    for i in range(key[0][0], key[1][0]):
        circuit.cnot(i+1, i)

    for i in range(length_key):
        if key[i][1] == 'X':
            circuit.h(key[i][0])
        elif key[i][1] == 'Y':
            circuit.rx(-np.pi/2, key[i][0])

    return circuit

def double_excitation(key, angle):

    # if name_angle is None:
    #     a_theta = Parameter('theta')
    # else:
    #     a_theta = Parameter(name_angle)

    num_qubits = key[3][0] - key[0][0] + 1
    length_key = len(key)

    circuit = QuantumCircuit(num_qubits)

    for i in range(length_key):
        if key[i][1] == 'X':
            circuit.h(key[i][0])
        elif key[i][1] == 'Y':
            circuit.rx(np.pi/2, key[i][0])
    
    for i in reversed(range(key[0][0], key[3][0])):
        circuit.cnot(i+1, i)
    
    circuit.rz(angle, 0)

    for i in range(key[0][0], key[3][0]):
        circuit.cnot(i+1, i)
    
    for i in range(length_key):
        if key[i][1] == 'X':
            circuit.h(key[i][0])
        elif key[i][1] == 'Y':
            circuit.rx(-np.pi/2, key[i][0])

    return circuit

def double_excitation_bis(excitation, angle):
    num_qubits = excitation[3] - excitation[0] + 1
    
    circuit = QuantumCircuit(num_qubits)

    #step 1
    circuit.h(3)
    circuit.h(2)
    circuit.rx(np.pi/2, 1)
    circuit.h(0)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.h(0)
    circuit.rx(-np.pi/2,1)
    circuit.h(2)
    circuit.h(3)

    #step 2
    circuit.h(3)
    circuit.h(2)
    circuit.rx(np.pi/2, 0)
    circuit.h(1)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.h(1)
    circuit.rx(-np.pi/2,0)
    circuit.h(2)
    circuit.h(3)

    #step 3
    circuit.h(3)
    circuit.rx(np.pi/2, 2)
    circuit.rx(np.pi/2, 1)
    circuit.rx(np.pi/2, 0)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.rx(-np.pi/2, 0)
    circuit.rx(-np.pi/2,1)
    circuit.rx(-np.pi/2, 2)
    circuit.h(3)

    #step 4 
    circuit.rx(np.pi/2, 3)
    circuit.h(2)
    circuit.rx(np.pi/2, 1)
    circuit.rx(np.pi/2, 0)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.rx(-np.pi/2, 0)
    circuit.rx(-np.pi/2,1)
    circuit.h(2)
    circuit.rx(-np.pi/2, 3)

    #step 5
    circuit.h(3)
    circuit.rx(np.pi/2, 2)
    circuit.h(1)
    circuit.h(0)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(-angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.h(0)
    circuit.rx(-np.pi/2,2)
    circuit.h(1)
    circuit.h(3)

    #step 6 
    circuit.h(1)
    circuit.h(2)
    circuit.rx(np.pi/2, 3)
    circuit.h(0)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(-angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.h(0)
    circuit.rx(-np.pi/2,3)
    circuit.h(2)
    circuit.h(1)

    #step 7 
    circuit.rx(np.pi/2, 3)
    circuit.rx(np.pi/2, 2)
    circuit.rx(np.pi/2, 0)
    circuit.h(1)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(-angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.h(1)
    circuit.rx(-np.pi/2,0)
    circuit.rx(-np.pi/2, 2)
    circuit.rx(-np.pi/2, 3)

    #step 8
    circuit.rx(np.pi/2, 3)
    circuit.rx(np.pi/2, 2)
    circuit.rx(np.pi/2, 1)
    circuit.h(0)

    for i in reversed(range(excitation[0], excitation[3])):
        circuit.cnot(i+1,i)
    
    circuit.rz(-angle, 0)

    for i in range(excitation[0], excitation[3]):
        circuit.cnot(i+1, i)
    
    circuit.h(0)
    circuit.rx(-np.pi/2,1)
    circuit.rx(-np.pi/2, 2)
    circuit.rx(-np.pi/2, 3)

    return circuit

def single_excitation_bis(excitation, angle):
    #num_qubits = excitation[1] - excitation[0] + 1
    num_qubits = 4

    circuit = QuantumCircuit(num_qubits)

    #Step 1 
    circuit.h(excitation[1])
    circuit.rx(np.pi/2, excitation[0])

    for i in reversed(range(excitation[0], excitation[1])):
        circuit.cnot(i+1,i)

    circuit.rz(angle, excitation[0])

    for i in range(excitation[0], excitation[1]):
        circuit.cnot(i+1, i)
    
    circuit.h(excitation[1])
    circuit.rx(-np.pi/2, excitation[0])

    #Step 2
    circuit.h(excitation[0])
    circuit.rx(np.pi/2, excitation[1])

    for i in reversed(range(excitation[0], excitation[1])):
        circuit.cnot(i+1,i)

    circuit.rz(-angle, excitation[0])

    for i in range(excitation[0], excitation[1]):
        circuit.cnot(i+1, i)
    
    circuit.h(excitation[0])
    circuit.rx(-np.pi/2, excitation[1])

    return circuit