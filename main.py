from flask import Flask, jsonify, request
import os
from router import handle_slash_command

app = Flask(__name__)

class SlackRequestData:
    def __init__(self, request_data):
        self.timestamp = request_data.get('headers', {}).get('x-slack-request-timestamp')
        self.signature = request_data.get('headers', {}).get('x-slack-signature')
        self.response_url = request_data.get('body', {}).get('response_url')
        self.text = request_data.get('body', {}).get('text')
        self.command = request_data.get('body', {}).get('command')
        self.user_id = request_data.get('body', {}).get('user_id')
        self.channel_id = request_data.get('body', {}).get('channel_id')
        self.channel_name = request_data.get('body', {}).get('channel_name')
        self.team_id = request_data.get('body', {}).get('team_id')
        self.trigger_id = request_data.get('body', {}).get('trigger_id')
        self.token = request_data.get('body', {}).get('token')

    def to_dict(self):
        return {
            'x-slack-request-timestamp': self.timestamp,
            'x-slack-signature': self.signature,
            'response_url': self.response_url,
            'text': self.text,
            'command': self.command,
            'user_id': self.user_id,
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'team_id': self.team_id,
            'trigger_id': self.trigger_id,
            'token': self.token,
        }


@app.route('/', methods=['POST'])

handle_slash_command()

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
