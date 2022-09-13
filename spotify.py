# Simple Python file for interacting with the Spotify Search API
import requests

'''
GET_TRACK_URL: Sends a request using the requests library to the Spotify Search API, parses the JSON response,
and returns the URL for the preview of the first track that matches the song title.
'''
def get_track_url(song_title):
    spotify_url = "https://api.spotify.com/v1/search"               # Spotify Search API endpoint
    params = {"q": song_title, "type": "track"}                     # Parameters for the request
    response = requests.get(spotify_url, params=params).json()      # Send the request and parse the JSON response
    track_url = response["tracks"]["items"][0]["preview_url"]       # Get the URL for the preview of the first track
    return track_url