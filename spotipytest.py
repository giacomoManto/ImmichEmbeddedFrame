import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
# Retrieve API key from .env
spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri="https://spotify.com", client_id=spotify_id, client_secret=spotify_secret, scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " - ", track['name'])