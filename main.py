from flask import Flask, jsonify, request, abort
import os
from router import handle_slash_command
from my_classes import SlackRequestData
from slack_verification import verify_slack_signature
import logging

app = Flask(__name__)
secret = os.environ.get('slack_signing_secret')

def logging_setup():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger
@app.route('/', methods=['POST'])
def handle_request():
    logging.info('Handling request')
    inbound_data = SlackRequestData(request.form, request.headers)
    print(inbound_data.to_dict())

    # Verify the Slack request signature
    logging.info('Sending payload to Verifying signature')
    if not verify_slack_signature(secret, inbound_data):
        abort(403)  # Forbidden if the signature verification fails

    #handle_slash_command(inbound_data)
    return jsonify({"status": "success"})

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
