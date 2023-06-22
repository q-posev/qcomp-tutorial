import numpy as np
import os

from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliOp
from qiskit.opflow.state_fns import CircuitStateFn, StateFn
from qiskit.opflow.expectations import PauliExpectation, AerPauliExpectation
from qiskit.opflow.converters import CircuitSampler

from openfermion import MolecularData
from openfermion.transforms import get_fermion_operator, jordan_wigner
from openfermionpyscf import run_pyscf
from openfermion.utils.operator_utils import count_qubits
from openfermion.circuits import uccsd_singlet_generator, uccsd_singlet_get_packed_amplitudes

def MoleculeSimulator(geometry, basis_set, multiplicity, charge, bond_length, occupied_indices, active_indices):
    molecule = MolecularData(geometry, basis_set, multiplicity, charge=charge, description='bondlength'+str(bond_length)+'A', filename=" ", data_directory= os.getcwd()+'/data')

    molecule = run_pyscf(molecule=molecule, run_scf=True, run_mp2=False, run_cisd=False, run_ccsd=True, run_fci=True, verbose=False)

    n_electrons = molecule.n_electrons

    molecular_hamiltonian = molecule.get_molecular_hamiltonian(occupied_indices=occupied_indices, active_indices=active_indices)

    f_ops = get_fermion_operator(molecular_hamiltonian)

    jw_f_ops = jordan_wigner(f_ops)

    qubit_hamiltonian = of_to_qiskit_op(jw_f_ops)

    return molecule, molecular_hamiltonian, f_ops, qubit_hamiltonian

def of_to_qiskit_op(qubit_operator):
    op = 0
    
    for qubit_terms, qubit_coeff in qubit_operator.terms.items():
        string_term = "I"*count_qubits(qubit_operator)
        for i, (term_qubit, term_pauli) in enumerate(qubit_terms):
            string_term = (string_term[:term_qubit] + term_pauli + string_term[term_qubit + 1 :])
        op += PauliOp(Pauli(string_term), coeff=qubit_coeff)
    return op

def expectation_value(pauli_operator, circuit, quantum_instance, shots, expectation):

    if shots > 0:
        quantum_instance.set_config(shots=shots)
    op = StateFn(pauli_operator, is_measurement=True)
    wfn = CircuitStateFn(circuit)
    opwfn = op @ wfn
    grouped = expectation.convert(opwfn)
    sampled_op = CircuitSampler(quantum_instance).convert(grouped)
    mean_value = sampled_op.eval().real

    return mean_value

def UCCSD_excitations_generator(molecule):
    electrons = molecule.n_electrons
    qubits = molecule.n_qubits

    ccsd_single_amps = molecule.ccsd_single_amps
    ccsd_double_amps = molecule.ccsd_double_amps

    singlet_amps = uccsd_singlet_get_packed_amplitudes(ccsd_single_amps, ccsd_double_amps, qubits, electrons)
    uccsd_singlet = uccsd_singlet_generator(singlet_amps, qubits, electrons)

    uccsd_jw = jordan_wigner(uccsd_singlet)

    return uccsd_jw