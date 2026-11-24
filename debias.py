import json
from pathlib import Path

data = json.loads(Path("bits.json").read_text())
bitstrings = data["bitstrings"]
bits = [int(b) for s in bitstrings for b in s]
print(f"{data['backend']}: {len(bits)} raw bits, zeros {bits.count(0) / len(bits):.2%}")

n = len(bitstrings[0])
per_qubit = [[int(s[i]) for s in bitstrings] for i in range(n)]
zeros = sorted(col.count(0) / len(col) for col in per_qubit)
print(f"per qubit: {zeros[0]:.1%} to {zeros[-1]:.1%} zeros")


def von_neumann(seq):
    out = []
    for a, b in zip(seq[0::2], seq[1::2]):
        if a != b:
            out.append(a)
    return out


same_qubit = [b for col in per_qubit for b in col]
clean = von_neumann(same_qubit)
print(f"after von Neumann: {len(clean)} bits, zeros {clean.count(0) / len(clean):.2%}")
