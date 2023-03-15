import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile, Aer
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
from math import pi
from Grover import diffuser_grover

#Quantum equivalent of a XOR gate
def XORgate(circuit, input_a, input_b, output):
    circuit.cx(input_a, output)
    circuit.cx(input_b, output)

#Definition of the Sudoku oracle, replacing the Grover's oracle
def sudoku_oracle(circuit, var_qubits, clause_qubits, output_qubit, qubits):
    i=0
    #Check rows consistency
    for a in range(qubits):
        for j in range(1,qubits):
            for b in range(j, qubits):
                XORgate(circuit, var_qubits[a*qubits + j -1], var_qubits[a*qubits + b], clause_qubits[i])
                i += 1
        circuit.barrier() 
    
    #Check columns consistency
    for c in range(qubits):
        for k in range(1, qubits, 1):
            for l in range(k, qubits):
                XORgate(circuit, var_qubits[c + (k-1)*qubits], var_qubits[l*qubits +c], clause_qubits[i])
                i +=1
        circuit.barrier()
    
    circuit.mct(clause_qubits, output_qubit)

#Definition of the circuit solving the Sudoku with several iterations of the Grover's algorithm
def Sudoku_circuit(circuit, iteration, var_qubits, clause_qubits, output_qubit, qubits, cbits):
    for i in range(iteration):
        total_qubits = n*N + 1
        circuit.append(sudoku_oracle(circuit, var_qubits, clause_qubits, output_qubit, qubits), range(total_qubits))
        circuit.barrier()
        circuit.append(diffuser_grover(qubits), range(qubits))
        circuit.barrier()
    return circuit


#Parameters of the simulation
n = 3 #number of different values per row/column
N = n*n #number of total different values == number of variable qubits
iterations = 2 #number of repetitions of the Grover's algorithm

#Definition of the different registers, either quantum or classical
var_qubits = QuantumRegister(N, name='v')
clause_qubits = QuantumRegister((n-1)*N, name='c')
output_qubit = QuantumRegister(1, name='out')
cbits = ClassicalRegister(N, name='cbits')

#Definition of the circuit used for the Grover algorithm to solve the sudoku
qc = QuantumCircuit(var_qubits, clause_qubits, output_qubit, cbits)

#Initialization of the circuit to the initial state
qc.initialize([1, -1]/np.sqrt(2), output_qubit)
qc.h(var_qubits)

for i in range(iterations):
    sudoku_oracle(qc, var_qubits=var_qubits, clause_qubits=clause_qubits, output_qubit=output_qubit, qubits=n)
    qc.barrier()
    qc.append(diffuser_grover(N),range(N))
    qc.barrier()

qc.measure(var_qubits, cbits)

qc.draw('mpl', filename='sudoku3x3_circ.png')