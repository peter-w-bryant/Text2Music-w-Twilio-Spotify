# Simple Python file for interacting with the Spotify Search API
import requests
'''
GET_TRACK_URL: Sends a request using the requests library to the Spotify Search API, parses the JSON response,
and returns the URL for the preview of the first track that matches the song title.
'''
def get_track_url(song_title, access_token):
    spotify_url = 'https://api.spotify.com/v1/search'  # The URL endpoint for the Spotify Search API.
    params = {'q': song_title, 'type': 'track'}        # The parameters for the request to the Spotify Search API.

    # Send a request to the Spotify Search API.
    spotify_response = requests.get(spotify_url, params=params, headers={'Authorization': 'Bearer ' + access_token}).json()

    track_url = spotify_response['tracks']['items'][0]['preview_url'] # Parse the JSON response to get the URL for the song preview.

    return track_url  # Return the URL for the song preview.

