import spotify

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
import urllib
import config

# Account SID and Auth Token from www.twilio.com/console
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
app = Flask(__name__)


# A route to respond to SMS messages and kick off a phone call.
@app.route('/sms', methods=['POST'])
def inbound_sms():
    response = MessagingResponse()
    response.message('Thanks for texting! Searching for your song now.'
                     'Wait to receive a phone call :)')

    # Grab the song title from the body of the text message.
    song_title = urllib.parse.quote(request.form['Body'])

    # Grab the relevant phone numbers.
    from_number = request.form['From']
    to_number = request.form['To']

    # Create a phone call that uses our other route to play a song from Spotify.
    client.api.account.calls.create(to=from_number, from_=to_number,
                        url='https://sms-service-twilio-spotify.herokuapp.com/call?track={}'
                        .format(song_title))

    return str(response)


# A route to handle the logic for phone calls.
@app.route('/call', methods=['POST'])
def outbound_call():
    song_title = request.args.get('track')
    track_url = spotify.get_track_url(song_title)

    response = MessagingResponse()
    response.play(track_url)
    return str(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)