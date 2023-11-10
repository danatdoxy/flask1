from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_slash_command():
    # Parse the incoming JSON from the Slack command
    data = request.form
    command = data.get('command')
    user_name = data.get('user_name')
    text = data.get('text')

    # Handle /summarize command
    if command == '/summarize':
        # This is where you would implement your summarization logic
        response_text = f"Summarization requested by {user_name}. You asked to summarize: {text}"

    # Handle /test command
    elif command == '/test':
        response_text = f"Test command received from {user_name}."

    else:
        response_text = f"The command {command} is not recognized."

    # Prepare the response for Slack
    response = {
        "response_type": "in_channel",  # or "ephemeral" for a private message
        "text": response_text,
    }

    return jsonify(response)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
