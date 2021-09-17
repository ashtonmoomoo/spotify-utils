import flask
from flask import request
import requests
import base64
import os
from spotipy import Spotify
import urllib

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID_A2L')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET_A2L')
REDIRECT_URI = 'http://localhost:5000' if os.environ.get('FLASK_DEBUG') == 'True' else 'https://album2library.herokuapp.com'

SCOPES = "user-library-read user-library-modify"

app = flask.Flask(__name__)

@app.get('/')
def home():
    if code := request.args.get('code'):
        token = get_access_token(code)
        client = Spotify(auth=token)
        songs = get_all_songs_from_albums(client)
        find_unliked_songs(client, songs)

        return """
            <p>if you can see this then it's probs done. check ur spotify</p>
        """

    else:
        return f"""
            <h2><b>Warning</b></h2>
            <h4>Clicking the log into spotify link and granting this app permissions will start the whole process without anymore input (I cbf making more buttons).</h4>
            <h4>Only click the button if you're sure you want to add all songs from the albums you have liked to your liked songs.</h4>
            <h5><i>It's not my fault if I mess up your library</i></h5>
            <a href=\"{make_url()}\">Click here to log into Spotify.</a></br></br>
            <a href=\"https://github.com/ashtonmoomoo/spotify-utils\">Source code here</a>
        """

def make_url():
    base = 'https://accounts.spotify.com/authorize?'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES
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
    next_exists = True

    while next_exists:
        albums = client.current_user_saved_albums(limit=max_albums, offset=offset)

        for album in albums.get("items"):
            songs += [track.get("uri") for track in album.get("album").get("tracks").get("items")]
        offset += max_albums

        next_exists = bool(albums.get("next"))

    return songs

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def find_unliked_songs(client, songs):
    for b in batch(songs, n=50):
        truth_array = client.current_user_saved_tracks_contains(b)
        songs_to_like = [b[i] for i in range(len(b)) if not truth_array[i]]
        if len(songs_to_like) > 0:
            client.current_user_saved_tracks_add(songs_to_like)

    return songs_to_like
