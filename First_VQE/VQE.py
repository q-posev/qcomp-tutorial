import numpy as np
import time
import os
from matplotlib import pyplot as plt

from qiskit.circuit import Parameter
from qiskit_aer import Aer
from qiskit.utils import QuantumInstance
from qiskit.opflow.expectations import PauliExpectation, AerPauliExpectation

from useful_functions import MoleculeSimulator, expectation_value, UCCSD_excitations_generator
from ansatze import HF_initial_state, UCCSD_ansatz, H2_UCCSD_ansatz

# Initialize variable to determine total run-time of the program
run_time = time.time()
# Set parameters primordial for the simulations
# bond lengths to simulate ground-state of H2 for (in Angstroms)
bond_lengths = np.arange(start=0.24, stop=3.0, step=0.1)
# no. of bond lengths to simulate H2 for
n_configs = len(bond_lengths)
print(f"INFO: Simulating ground-state of H2 molecule for {n_configs} bond lengths")
# no. of VQE parameter values to scan
n_theta = 24
# no. of shots for measurements on quantum device
n_shots = 2000

simulator = Aer.get_backend('statevector_simulator')
backend = QuantumInstance(backend = simulator)

#Setting up the molecule informations
def geometry(dist):
    geometry = [('Li', (0.0, 0.0, 0.0)), ('H', (0.0, 0.0, dist))]
    return geometry
#set the basis set used
basis_set = 'sto-3g'
#Set the multiplicity
multiplicity = 1
#total charge
charge = 0
# number of active electrons and orbitals to consider : for H2 as we're consider all electrons and orbitals as active for STO-3G
occ_ind = act_ind = None

mol_s_q = {}
mol_s_q_ops = {}
mol_configs = {}
mol_uccsd_exci = {}

for dist in bond_lengths:
    r = round(dist,2)
    print(f"INFO: Simulating ground-state of LiH molecule for bond-length {r} A...")

    geometry_fixed = geometry(r)

    (molecule, molecular_hamiltonian, f_ops, qubit_hamiltonian) = MoleculeSimulator(geometry_fixed, basis_set, multiplicity, charge, r, occ_ind, act_ind)

    mol_uccsd_exci[r] = [UCCSD_excitations_generator(molecule)]
    mol_s_q[r] = [molecule, molecular_hamiltonian]
    mol_s_q_ops[r] = [f_ops]
    mol_configs[r] = [molecule, qubit_hamiltonian]

    qubits = molecular_hamiltonian.n_qubits
    electrons = molecule.n_electrons

print(f"INFO: Simulating ground-state of LiH molecule for {len(mol_configs)} bond lengths")

initial_state = HF_initial_state(qubits, electrons)
a_theta = Parameter('a_theta')

fci_energy = []
for val in mol_configs.values():
    fci_energy.append(val[0].fci_energy)

for i in mol_configs:
    int_fci = 0
    print(f"INFO: Computing ground-state energy for bond length {i} A...")
    mol_configs[i].append(np.inf)
    for theta in np.linspace(start=-np.pi, stop=np.pi, num=n_theta, endpoint=True):
        ansatz = UCCSD_ansatz(qubits, initial_state, mol_uccsd_exci[i], a_theta)
        bind_ansatz = ansatz.bind_parameters({a_theta: theta})
        exp_H_theta = expectation_value(mol_configs[i][1], bind_ansatz, backend, n_shots, AerPauliExpectation())
        if exp_H_theta < mol_configs[i][2]:
            mol_configs[i][2] = exp_H_theta
    print(f"min {i} A ==> {mol_configs[i][2]:.8f} Ha")
    print(f"min {i} A) ==> {mol_configs[i][0].fci_energy:.8f} Ha")
    int_fci += 1

# Plot ground-state energy for each configuration vs bond length
plt.figure(figsize=(8,6), dpi=700)
#plt.plot(list(mol_configs.keys()), [val[0].hf_energy for val in mol_configs.values()], label='HF')
plt.plot(list(mol_configs.keys()), [val[0].fci_energy for val in mol_configs.values()], label='FCI')
plt.plot(list(mol_configs.keys()), [val[2] for val in mol_configs.values()], 'x-', label='VQE_ansatz')
plt.grid()
plt.xlabel('Bond length of LiH [A]')
plt.ylabel('Ground-state energy for LiH [Ha]')
plt.legend()
plt.title('VQE computed ground-state energy of LiH vs bond-length for STO-3G basis vs HF and FCI')
plt.savefig('LiH_PES_byVQE.png')
run_time = time.time()-run_time
print(f"Total running time : {run_time:.4f} s")
