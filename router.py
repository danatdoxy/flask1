import os
import json
from flask import Flask, jsonify, request
from my_classes import SlackRequestData
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def handle_slash_command():
    # Parse the incoming JSON from the Slack command
    command = SlackRequestData.command
    user_id = SlackRequestData.user_id
    text = SlackRequestData.text

    # Handle /summarize command
    if command == '/summarize':
        logging.info('Summarizing')
        # This is where you would implement your summarization logic
        response_text = f"Summarization requested by {user_id}. You asked to summarize: {user_id}"

    # Handle /test command
    elif command == '/test':
        logging.info('Testing')
        response_text = f"Test command received from {user_id}."

    else:
        logging.info('Command not recognized')
        response_text = f"The command {command} is not recognized."

    # Prepare the response for Slack
    response = {
        "response_type": "in_channel",  # or "ephemeral" for a private message
        "text": response_text,
    }

    return jsonify(response)