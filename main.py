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
    app.logger.info(f"Received a message event: {event}")
    # You can use `say` to send a message to the same channel

    if 'text' in event:
        text = event['text']
        app.logger.info('Text: ' + text)
        # Implement logic based on the message

@app.action("button_click")
def handle_button_clicks(body, ack, say):
    ack()  # Acknowledge button click event
    # Implement your logic for button click
    say(f"Button clicked!")

def handle_app_home_opened(event, client):
    user_id = event['user']
    try:
        app.logger.info(f"Received {user_id} app_home_opened event: {event}")

        # Construct the view payload
        view_payload = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "block_id": "r++V0",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Jarvis is an experimental internal tool for <http://doxy.me|doxy.me>\n\n *What you can do with Jarvis in the future:*",
                        "verbatim": False,
                    },
                },
                {"type": "divider", "block_id": "jxKR4"},
                {
                    "type": "section",
                    "block_id": "g6fCh",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Summerize Threads*\nSometimes conversations can get really lengthy. The /summerize command is a tool that makes it easy to get the inside scope without spending any more time than you need to getting caught up.",
                        "verbatim": False,
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://v5.airtableusercontent.com/v2/22/22/1698472800000/aCVNL0hu5rImksqRW9kchg/MrxWegGU2OEiBhqvPjFsn6FdtDQTrQMyXE76uo_cmrcGY1dKpHzY8WyUAw1qqIBDVGSK642yuuiO9OAVPB716jR83cgusKzU1Li2Ji900g_AtR4malMVwLWLxm_a-r8nS0dOuThwK1523x6osciRFQ/LPTpghQkzJeBPH0iZ61GoVzVOO-QlNs57fUYQemoIwo",
                        "alt_text": "alt text for image",
                    },
                },
                {
                    "type": "section",
                    "block_id": "g7jBH",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Use GPT 4*\nAlthough not as amazing as ChatGPT you can use the same exact Language Model that powers chatGPT right from slack.",
                        "verbatim": False,
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://v5.airtableusercontent.com/v2/22/22/1698472800000/v-jHcvYc7fdKeZZRTEozIw/I0Ppt_NTRg8M7O-04Jxbowy0Yu4VqbzYGVkeD6-jWXYFjFdRqkhMKrGffDmUr44qi5KeOkZuiAO2AlfQMLzFdQl0hfEd-g4mr0PuIMS6yKlhJqOBCYeHW-8o8gAHSCmpkgEnlFL3jySAWh6G6E6woQ/jEKMhYtG0WPmCWzc1EQTXnA8z4S_CrVAg3Qre6Ld6yM",
                        "alt_text": "alt text for image",
                    },
                },
                {
                    "type": "section",
                    "block_id": "mMY6L",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Get Data Insights*\nAsk questions about <http://doxy.me|doxy.me> data and get answers quickly and powerfully. This is powered by snowflake and OpenAI's GPT models",
                        "verbatim": False,
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://v5.airtableusercontent.com/v2/22/22/1698472800000/h-TK5jOQ_101PIUUzyrD2A/QAo0EN8hutVTzpURaQRjxulxUwk811601zxKMYWTYeYuGeDzPls0Df6YlR2owKx5PK3ev0bNuDkNL6GIE_20FllTLBdYlvoo_ERgTMUBi_a6WxurudkESjSEf0qbxMsWVyT2Ewb7hNDUuYFXMUUa-w/0glrNa9vNvOTbCLJXwdls-5yCNVILaXkDcgB0RvkH5M",
                        "alt_text": "alt text for image",
                    },
                },
            ],
        }

        # Publish the view to the App Home
        client.views_publish(
            user_id=user_id,
            view=view_payload
        )

    except Exception as e:
        app.logger.error(f"Error updating App Home: {e}")
@app.event({"type": re.compile(r".*")})
def handle_all_events(payload):
    app.logger.info(f"Received event: {payload}")

@flask_app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    flask_app.logger.addHandler(logging.StreamHandler(sys.stdout))
    flask_app.logger.setLevel(logging.ERROR)
    flask_app.run(debug=True, port=os.getenv("PORT", default=5000))