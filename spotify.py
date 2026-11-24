import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from debias import data
from shuffle import save_position, shuffle

PLAYLIST_NAME = "ah"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "playlist-read-private playlist-read-collaborative playlist-modify-private"

load_dotenv()
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=REDIRECT_URI,
        scope=SCOPES,
    )
)

playlists = sp.current_user_playlists()["items"]

source = next(p for p in playlists if p["name"] == PLAYLIST_NAME)
page = sp.playlist_items(source["id"])
entries = page["items"]
while page["next"]:
    page = sp.next(page)
    entries.extend(page["items"])
tracks = [e["item"] for e in entries if e["item"] and not e["is_local"]]
print(f"{source['name']}: {len(tracks)} of {page['total']} tracks")
for t in tracks[:5]:
    print(f"  {t['name']} - {t['artists'][0]['name']}")

shuffled = shuffle(tracks)
print("quantum order:")
for t in shuffled[:5]:
    print(f"  {t['name']} - {t['artists'][0]['name']}")


name = f"quantum shuffle: {source['name']}"
target = next((p for p in playlists if p["name"] == name), None)
if target is None:
    target = sp.current_user_playlist_create(name, public=False)

uris = [t["uri"] for t in shuffled]
sp.playlist_replace_items(target["id"], uris[:100])
for start in range(100, len(uris), 100):
    sp.playlist_add_items(target["id"], uris[start : start + 100])
save_position()


def repeats(songs):
    ids = [s["artists"][0]["id"] for s in songs]
    return sum(a == b for a, b in zip(ids, ids[1:]))


seconds = data["qpu_seconds"]
print(f"QPU time: {seconds} s, would have cost ${seconds * 1.60:.2f}")
print(f"artist repeats: {repeats(tracks)} yours -> {repeats(shuffled)} quantum")
print(f"playlist: {target['external_urls']['spotify']}")
