import flask
from flask import request
import requests
import base64
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import urllib

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID_A2L')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET_A2L')
REDIRECT_URI = 'http://localhost:5000'

SCOPE = "user-library-read"

app = flask.Flask(__name__)

@app.get('/')
def home():

    if code := request.args.get('code'):
        token = get_access_token(code)
        client = Spotify(auth=token)
        albums = get_all_songs_from_albums(client)
        return f"""
            <p>{albums}</p>
        """
    else:
        return f"<a href=\"{make_url()}\">Click here to log into Spotify.</a>"

def make_url():
    base = 'https://accounts.spotify.com/authorize?'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    return base + urllib.parse.urlencode(params)

def get_access_token(code):


    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Authorization': 'Basic ' + base64.b64encode((CLIENT_ID + ':'+ CLIENT_SECRET).encode('ascii')).decode('ascii')
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)

    token = ''
    if response.status_code == 200:
        token = response.json().get('access_token', '')

    return token

def get_all_songs_from_albums(client):
    songs = []
    max_albums = 50
    offset = 0

    albums = client.current_user_saved_albums(limit=max_albums, offset=offset)

    songs += [track.get("uri") for track in albums.get("items")[0].get("album").get("tracks").get("items")]

    return songs
