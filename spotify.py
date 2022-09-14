# Simple Python file for interacting with the Spotify Search API
import requests

'''
GET_TRACK_URL: Sends a request using the requests library to the Spotify Search API, parses the JSON response,
and returns the URL for the preview of the first track that matches the song title.
'''
def get_track_url(song_title, access_token):
    spotify_url = 'https://api.spotify.com/v1/search'
    params = {'q': song_title, 'type': 'track'}
    spotify_response = requests.get(spotify_url, params=params, headers={'Authorization': 'Bearer ' + access_token}).json()
    track_url = spotify_response['tracks']['items'][0]['preview_url']
    return track_url

