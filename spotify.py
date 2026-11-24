import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

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
for p in playlists:
    print(p["name"])

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
