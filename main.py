from flask import Flask, jsonify, request
import os
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from slack_sdk import WebClient

from slack_verification import OpenAIChatHandler, SlackHandler
import sys
import re
from openai import OpenAI #1.1.1
import logging

# Set up logging
logger = logging.getLogger('slack_app') #the getLogger() method returns a logger with the specified name if it exists already, or creates it.
logger.setLevel(logging.INFO) #set the logging level of this logger to INFO
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

client = OpenAI(api_key=os.environ.get("openai_key"))

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("slack_bot_token"),
    signing_secret=os.environ.get("slack_signing_secret")
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app) #notes
openai_handler = OpenAIChatHandler(os.environ.get("openai_key"))
slack_client = WebClient(token=os.environ.get("slack_bot_token"))
slack_handler = SlackHandler(os.environ.get("slack_bot_token"))

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    logger.info(f'Handling request: {request}')
    logger.info(f'Full request data: {request.get_data(as_text=True)}')  # Log the full raw request data
    return handler.handle(request)

@app.command("/summarize")
def handle_summarize_command(ack, body, say):
    ack()  # Acknowledge the command request immediately
    try:
        logger.info('Slash Command: summarize')
        logger.info(body)
        say("Processing summarize command...")  # Respond to the user
        # Implement your command logic here
        # body contains all the command information
    except Exception as e:
        logger.error(f"Error in summarize command: {e}")


@app.shortcut('summerize-thread')
def handle_summarize_thread(ack, body, client, logger):
    ack()  # Acknowledge the message action request immediately
    try:
        logger.info('Message Action: summarize-thread')
        logger.info(body)

        # Fetch necessary details from body
        channel_id = body['channel']['id']
        message_ts = body['message_ts']  # Timestamp of the message where the action was triggered

        # Retrieve all the threads for the ts
        thread_history = slack_handler.get_thread_history(channel_id, message_ts)
        chat_array = slack_handler.build_chat_array(thread_history, system_message="Summarize the user's Slack conversation thread", as_string=True)


        # Send the combined messages to OpenAI and get the response
        summary = openai_handler.send_thread_to_openai(chat_array)

        # Post the summary as an ephemeral message
        client.chat_postEphemeral(channel=channel_id, user=body['user']['id'], text=summary)

    except Exception as e:
        logger.error(f"Error in summarize-thread message action: {e}")
@app.event("message")
def handle_message_events(body, say, event):
    user_id = event.get('user')
    channel_id = event.get('channel')
    thread_ts = event.get('thread_ts', None)
    bot_id = event.get('bot_id', None)

    if bot_id:
        return

    text = event.get('text', '')

    if not thread_ts:
        # If it's a new message, set thread_ts to the timestamp of this message
        thread_ts = event.get('ts')

    # Handle as a threaded message
    thread_history = slack_handler.get_thread_history(channel_id, thread_ts)
    chat_array = slack_handler.build_chat_array(thread_history)
    response = openai_handler.send_thread_to_openai(chat_array)
    slack_client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=response)

@app.action("button_click")
def handle_button_clicks(body, ack, say):
    ack()  # Acknowledge button click event
    # Implement your logic for button click
    say(f"Button clicked!")

@app.event("app_home_opened")
def handle_app_home_opened(event, client):
    user_id = event['user']
    try:
        logger.info(f"Received {user_id} app_home_opened event: {event}")

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
        logger.error(f"Error updating App Home: {e}")
@app.event({"type": re.compile(r".*")})
def handle_all_events(payload):
    logger.info(f"Received event: {payload}")

@flask_app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    flask_app.run(debug=True, port=os.getenv("PORT", default=5000))