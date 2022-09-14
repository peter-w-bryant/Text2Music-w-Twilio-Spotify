# General Modules
from flask import Flask, request, url_for, session, redirect
import urllib
# Spotify/Spotipy
import spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Twilio
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
# Config (SECRET)
import config

# Account SID and Auth Token from www.twilio.com/console
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

app = Flask(__name__)
app.secret_key = config.secret_key

# SMS (Text): A route to respond to SMS messages with song titles and send a phone call.
@app.route('/sms', methods=['POST'])
def inbound_sms():
    response = MessagingResponse()                                                           # Create a response object
    response.message('Song request received - we are searching for the song now.'            # Send a response text message to the user
                     ' Wait for a phone call and follow the prompt to listen to the song.')
                     
    song_title = urllib.parse.quote(request.form['Body'])   # Access the song title from the body of the text message.
    from_number = request.form['From']                      # Access the phone number of the user who sent the text message.
    to_number = request.form['To']                          # Access the phone number of the Twilio number that received the text message.

    # Create a phone call that uses a public URL to play a song from Spotify.
    client.api.account.calls.create(to=from_number, from_=to_number,
                        url='{}/call?track={}'
                        .format(config.pub_url, song_title))

    return str(response)  # Return the response object as a string.
 
# CALL: A route to handle the logic for the phone call.
@app.route('/call', methods=['POST'])
def outbound_call():
    song_title = request.args.get('track')                              # Access the song title from the URL query string.
    track_url = spotify.get_track_url(song_title, config.access_token)  # Get the URL for the song preview from Spotify.
    response = VoiceResponse()                                          # Create a Voice response object.
    response.play(track_url)                                            # Play the song preview from Spotify.
    return str(response)                                                # Return the response object as a string.

"""
Function to create a SpotifyOAuth object. This object is used to authenticate the user with Spotify, unused as of now
because an access token is already generated and stored in config.py!
"""
def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=config.client_id,
            client_secret=config.client_secret, 
            redirect_uri=url_for('authorize', _external=True),
            scope=config.scope)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)