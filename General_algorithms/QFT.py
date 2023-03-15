import numpy as np
from qiskit import QuantumCircuit, assemble, Aer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_qsphere
from qiskit.quantum_info import Statevector
from math import sqrt, pi

#Definition of the simulator used in the compilation
sim = Aer.get_backend('aer_simulator')

#Definition of a function for our rotation angle
def theta(n,k):
    return  pi/(2**(n-k))

#Definition of the Quantum Fourier Transform circuit
def QFT(n):
    #Initiate a circuit
    circuit = QuantumCircuit(n)
    #Loops that apply the necessary gates for our circuit
    for i in reversed(range(n)):
        circuit.h(i)
        for j in range(i):
            circuit.cp(theta(i,j), j, i)
    #Loop that apply the necessary swap at the end of the circuit    
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)

    return circuit

#Creation of our initial circuit
init = QuantumCircuit(4)
init.x(2)
init.x(3)

#Save the initial statevector of our system
qc_init = init.copy()
qc_init.save_statevector()
init_state = sim.run(qc_init).result().get_statevector()

#Define a circuit, as the sum of an initial circuit (use to define the wanted states) with our QFT circuit
qc = init + QFT(4)

#Different prints (in the shell and in a mpl file) of our circuit
print(qc)
qc.draw('mpl', filename='QFT_example.png')

qc.save_statevector()
final_state = sim.run(qc).result().get_statevector()

plot_bloch_multivector(init_state, filename='QFTinitstate.png')
plot_bloch_multivector(final_state, filename='QFTfinalstate.png')
