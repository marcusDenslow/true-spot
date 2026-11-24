import json
import os
from pathlib import Path

from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService

JOB_FILE = Path("job_id.txt")
CACHE_FILE = Path("bits.json")

load_dotenv()
service = QiskitRuntimeService(
    channel="ibm_quantum_platform",
    token=os.environ["IBM_QUANTUM_TOKEN"],
    instance=os.environ["IBM_QUANTUM_INSTANCE"],
)

job = service.job(JOB_FILE.read_text().strip())
print(f"job {job.job_id()} on {job.backend().name}: {job.status()}")

t = job.metrics()["timestamps"]
print(f"created {t['created']}")
print(f"running {t['running']}")
print(f"finished {t['finished']}")

result = job.result()
bitstrings = result[0].data.meas.get_bitstrings()
qpu_seconds = job.usage()
CACHE_FILE.write_text(
    json.dumps(
        {
            "job_id": job.job_id(),
            "backend": job.backend().name,
            "qpu_seconds": qpu_seconds,
            "bitstrings": bitstrings,
        }
    )
)
print(f"cached {len(bitstrings)} shots. QPU time: {qpu_seconds} s")
