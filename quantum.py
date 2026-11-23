from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

N_QUBITS = 16
SHOTS = 100
qc = QuantumCircuit(N_QUBITS)
qc.h(range(N_QUBITS))
qc.measure_all()
print(qc)

sampler = StatevectorSampler()
job = sampler.run([qc], shots=SHOTS)
result = job.result()
bitstrings = result[0].data.meas.get_bitstrings()
bits = [int(b) for s in bitstrings for b in s]

print(f"{len(bits)} bits")
print(f"zeros: {bits.count(0) / len(bits):.2%}")
print("".join(str(b) for b in bits[:64]))
