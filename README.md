# true-spot

shuffles a spotify playlist using random bits from a real IBM quantum computer instead of spotify's shuffle, which isn't actually random.

how it works:

- 100 qubits with a hadamard on each, measured 1000 times on IBM hardware, gives 100k random bits
- von neumann debiasing per qubit, which throws away about 75% of them
- fisher-yates shuffle on the rest, with rejection sampling to avoid modulo bias
- the new order gets written into a spotify playlist

the quantum job used 2 seconds of QPU time, which would be $3.20 on IBM's pay as you go plan.

## running it

you need an IBM Quantum account (free plan works) and spotify premium, since the spotify dev API requires it.

put your keys in `.env`:

```
IBM_QUANTUM_TOKEN=
IBM_QUANTUM_INSTANCE=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

add `http://127.0.0.1:8888/callback` as a redirect uri in your spotify app.

```
pip install qiskit qiskit-ibm-runtime spotipy python-dotenv
python submit.py    # sends the job to IBM, only runs once unless you delete job_id.txt
python fetch.py     # downloads the bits into bits.json
python spotify.py   # set PLAYLIST_NAME first
```

play the playlist with shuffle off. bits.json from my run is included, so you can skip the IBM part and just run spotify.py. each run uses new bits, so you get a different order every time.
