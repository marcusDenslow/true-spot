# true-spot

spotify shuffle isn't actually random (they admitted it in 2014) so i made my own using a real IBM quantum computer. completely normal thing to do

how it works:

- 100 qubits, hadamard on each, measured 1000 times on IBM hardware. 100k random bits
- von neumann debiasing per qubit, throws away like 75% of them
- fisher-yates shuffle on whats left, with rejection sampling so theres no modulo bias
- writes the new order into a spotify playlist

the quantum part used 2 seconds of QPU time. pay as you go thats $3.20. for a playlist

## running it

you need an IBM Quantum account (free plan is fine) and spotify premium, because their dev API requires it now. yes really

`.env`:

```
IBM_QUANTUM_TOKEN=
IBM_QUANTUM_INSTANCE=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

set the redirect uri in your spotify app to `http://127.0.0.1:8888/callback`

```
pip install qiskit qiskit-ibm-runtime spotipy python-dotenv
python submit.py    # sends the job to IBM. locks itself after, delete job_id.txt to send another
python fetch.py     # downloads the bits into bits.json
python spotify.py   # change PLAYLIST_NAME first. play with shuffle OFF
```

my bits.json is in the repo so you can skip the quantum part and just run spotify.py. every run uses fresh bits so you get a new order each time
