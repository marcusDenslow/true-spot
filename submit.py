import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

N_QUBITS = 100
SHOTS = 1000
SUBMIT = True
JOB_FILE = Path("job_id.txt")

if JOB_FILE.exists():
    sys.exit(f"already submitted: {JOB_FILE.read_text()}. not burning more quota")


load_dotenv()
service = QiskitRuntimeService(
    channel="ibm_quantum_platform",
    token=os.environ["IBM_QUANTUM_TOKEN"],
    instance=os.environ["IBM_QUANTUM_INSTANCE"],
)

backend = service.least_busy(operational=True, simulator=False, min_num_qubits=N_QUBITS)
print(f"backend: {backend.name} ({backend.num_qubits}) qubits")
print(f"jobs in line: {backend.status().pending_jobs}")

qc = QuantumCircuit(N_QUBITS)
qc.h(range(N_QUBITS))
qc.measure_all()

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa = pm.run(qc)
print(f"isa: {isa.num_qubits} qubits, depth {isa.depth()}, ops {dict(isa.count_ops())}")

if not SUBMIT:
    print("dry run. flip SUBMIT to send it for real")
    sys.exit()

sampler = SamplerV2(mode=backend)
job = sampler.run([isa], shots=SHOTS)
JOB_FILE.write_text(job.job_id())
print(f"submitted: {job.job_id()}")
print(f"status: {job.status()}")
