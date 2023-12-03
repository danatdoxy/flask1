from flask import Flask, jsonify, request
import os
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
import logging
import sys
import re
from openai import OpenAI #1.1.1

client = OpenAI(api_key=os.environ.get("openai_key"))

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("slack_bot_token"),
    signing_secret=os.environ.get("slack_signing_secret")
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

client = src.client_key(scrapebee_api_key,openai_api_key)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    flask_app.logger.info('Handling request')
    flask_app.logger.info(request)
    return handler.handle(request)

@app.command("/summarize")
def handle_summarize_command(ack, body, say):
    ack()  # Acknowledge the command request immediately
    try:
        app.logger.info('Slash Command: summarize')
        app.logger.info(body)
        say("Processing summarize command...")  # Respond to the user
        # Implement your command logic here
        # body contains all the command information
    except Exception as e:
        app.logger.error(f"Error in summarize command: {e}")

@app.event("message")
def handle_message_events(event, say):
    # Log the event
    logging.info(f"Received a message event: {event}")
    # You can use `say` to send a message to the same channel
    say(f"Received a message event: {event}")
    if 'text' in event:
        text = event['text']
        app.logger.info('Text: ' + text)
        # Implement logic based on the message

@app.action("button_click")
def handle_button_clicks(body, ack, say):
    ack()  # Acknowledge button click event
    # Implement your logic for button click
    say(f"Button clicked!")

@app.event("app_home_opened")
def handle_app_home_opened(event, client):
    # Handle the app home opened event
    user_id = event['user']
    try:
        logging.info(f"Received {user_id} app_home_opened event: {event}")
        # Update the App Home for the user
    except Exception as e:
        logging.error(f"Error updating App Home: {e}")
@app.event({"type": re.compile(r".*")})
def handle_all_events(payload, say, logging):
    logging.info(f"Received event: {payload}")

@flask_app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    flask_app.logger.addHandler(logging.StreamHandler(sys.stdout))
    flask_app.logger.setLevel(logging.ERROR)
    flask_app.run(debug=True, port=os.getenv("PORT", default=5000))