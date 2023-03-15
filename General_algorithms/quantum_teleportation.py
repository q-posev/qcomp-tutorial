import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector

#Set up of the protocol : 3 qubits and 2 classical bits (in two different registers)
qubits = QuantumRegister(3, name="q")
crz = ClassicalRegister(1, name="crz")
crx = ClassicalRegister(1, name="crx")

circuit = QuantumCircuit(qubits, crz, crx)

#Set up of a random state for the initial Alice's qubit
psi = random_statevector(2)

print(psi)
plot_bloch_multivector(psi, filename='quteleportstate.png')

#Create a gate that initialize a qubit as the random state defined above
init_gate = Initialize(psi)
init_gate.label = "init"

#Definition of a function creating the wanted initial state for Alice's qubit
def initialization(qc, gate, qubits):
    qc.append(gate, range(qubits))
    qc.barrier()

#Step 1 : Telamon creates the needed entangled pair, that will be associated with the qubit owned by Alice
def Bell_pair(qc, a, b):
    qc.h(a)
    qc.cx(a,b)
    qc.barrier()

#Step 2 : Alice applies a CNOT gate on her two qubits, followed by a Hamadard gate on her first qubit
def Alice_gate(qc, psi, a):
    qc.cx(psi, a)
    qc.h(psi)
    qc.barrier()

#Step 3 : Alice measures her two qubits and send them as classical bits to Bob
def measure_and_send(qc, a, b):
    qc.measure(a,0)
    qc.measure(b,1)

#Step 4 : Bob applies the needed gate to determine the qubit he received from Alice
def Bob_gate(qc, qubit, z, x):
    qc.x(qubit).c_if(x, 1)
    qc.z(qubit).c_if(z, 1)


#Concrete implementation of this protocol
initialization(circuit, init_gate, 1)
Bell_pair(circuit, qubits[1], qubits[2])
Alice_gate(circuit, qubits[0], qubits[1])
measure_and_send(circuit, qubits[0], qubits[1])
Bob_gate(circuit, qubits[2], crz, crx)

print(circuit.draw(justify='none'))
circuit.draw('mpl', justify='none', filename='quteleport_circuit.png')

#Simulation of the quantum teleportation algorithm
sim = Aer.get_backend('qasm_simulator')
circuit.save_statevector()
out_vector = sim.run(circuit).result().get_statevector()

plot_bloch_multivector(out_vector, filename='quteleport_outstate.png')

#In a real quantum computer, we would not be able to access the statevector. So to check if our protocol is working, we work in reverse :
#We expect to measure with certainty, on the qubit of Bob at the end, it on the state |0> if we perform before the measurement the inverse of the unitary
#operation that initialize the state of Alice in the random statevector |psi>