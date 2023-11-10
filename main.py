from flask import Flask, jsonify, request
import os
from router import handle_slash_command
from my_classes import SlackRequestData
app = Flask(__name__)



@app.route('/', methods=['POST'])
inbound_data = SlackRequestData(request.form, request.headers)
handle_slash_command(inbound_data)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
