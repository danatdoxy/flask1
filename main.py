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
    # The body of the request needs to be obtained from request.get_data() or similar
    body = request.get_data(as_text=True)  # Get the raw body of the request
    # print(inbound_data.to_dict())

    logging.info('Sending payload to Verifying signature')
    # Pass the secret, the inbound_data object, and the raw body to the verification function
    if not verify_slack_signature(secret, inbound_data, body):
        abort(403)  # Forbidden if the signature verification fails

    # Handle the slash command
    return jsonify({"status": "success"})

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
