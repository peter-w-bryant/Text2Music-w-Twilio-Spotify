import spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.twiml.voice_response import Play, VoiceResponse
from twilio.rest import Client
import urllib
import config

# Account SID and Auth Token from www.twilio.com/console
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

app = Flask(__name__)
app.secret_key = config.secret_key

# Create a route to authenticate the current user
@app.route("/", methods=['POST', 'GET'])
def OAuth():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


# Create a route to authenticate the current user
@app.route("/authorize", methods=['POST', 'GET'])
def authorize():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token = sp_oauth.get_access_token(code)
    access_token = token['access_token']
    session['access_token'] = access_token
    return redirect(url_for('inbound_sms'))


# A route to respond to SMS messages and kick off a phone call.
@app.route('/sms', methods=['POST'])
def inbound_sms():
    response = MessagingResponse()
    response.message('Thanks for texting! Searching for your song now.'
                     ' Wait to receive a phone call :)')

    # Grab the song title from the body of the text message.
    song_title = urllib.parse.quote(request.form['Body'])

    # Grab the relevant phone numbers.
    from_number = request.form['From']
    to_number = request.form['To']

    # Create a phone call that uses our other route to play a song from Spotify.
    client.api.account.calls.create(to=from_number, from_=to_number,
                        url='https://1ddc-50-93-222-84.ngrok.io/call?track={}'
                        .format(song_title))
    return str(response)


# A route to handle the logic for phone calls.
@app.route('/call', methods=['POST'])
def outbound_call():
    song_title = request.args.get('track')
    track_url = spotify.get_track_url(song_title, config.access_token)
    response = VoiceResponse()
    response.play(track_url)
    return str(response)

"""
Function to create a SpotifyOAuth object. This object is used to authenticate the user with Spotify. The scope determines what data we can access.
In our case, we want the user-library-read scope, which allows us to read the user's saved tracks.
"""
def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=config.client_id,
            client_secret=config.client_secret, 
            redirect_uri=url_for('authorize', _external=True),
            scope="user-library-read user-read-recently-played user-read-private user-top-read user-read-currently-playing")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)