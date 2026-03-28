import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Manually set your credentials here for this one-time check
os.environ['SPOTIPY_CLIENT_ID'] = 'd6e04f62f42a41859e3f0303da93275d'
os.environ['SPOTIPY_CLIENT_SECRET'] = '0f83fb5786fa481c8ae02a4254d0e056'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8888/callback'

scope = "user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))

# This will trigger the prompt
print("Getting user info...")
user = sp.current_user()
print(f"Success! Linked to: {user['display_name']}")
