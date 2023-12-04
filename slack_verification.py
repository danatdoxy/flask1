
import sys
from openai import OpenAI
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class OpenAIChatHandler:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    def send_message_to_openai(self, slack_event: dict):
        logging.info('Sending message to openai')

        # Extract the message content from the Slack event
        user_message = slack_event.get("text", "")

        # Create the system and user messages for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]

        # Send the messages to OpenAI and get the response
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Return the OpenAI response
        return completion.choices[0].message.content

    def send_thread_to_openai(self, chat_array):
        # Send the messages to OpenAI and get the response
        logging.info('Sending thread to openai')
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_array
        )
        # Access the 'content' attribute directly from the 'message' object
        response = completion.choices[0].message.content  # Instead of ['content']
        logging.info(f'Chat response is:\n {response}')
        return response

class SlackHandler:
    def __init__(self, token: str):
        self.client = WebClient(token=token)

    def get_thread_history(self, channel: str, thread_ts: str):
        logging.info('Setting messaging history')
        messages = []
        try:
            # Initial call to conversations.replies
            response = self.client.conversations_replies(channel=channel, ts=thread_ts, limit=200)
            messages.extend(response['messages'])

            # Loop through pagination if more messages are available
            while response['response_metadata']['next_cursor']:
                response = self.client.conversations_replies(
                    channel=channel,
                    ts=thread_ts,
                    cursor=response['response_metadata']['next_cursor'],
                    limit=200
                )
                messages.extend(response['messages'])

        except SlackApiError as e:
            logging.error(f"Error fetching conversation replies: {e.response['error']}")
        return messages

    def post_message(self, channel: str, thread_ts: str, message: str):
        logging.info('Sending message to slack')
        try:
            self.client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=message)
        except SlackApiError as e:
            logging.error(f"Error posting message: {e.response['error']}")

    def build_chat_array(self, messages):
        """
        Builds an array of chat messages formatted for OpenAI input.

        Parameters:
        messages (list): A list of message dicts from Slack.

        Returns:
        list: A list of formatted chat messages for OpenAI.
        """
        logging.info('Building chat array')

        # Define the initial system message
        chat_array = [{"role": "system", "content": "You are a helpful assistant."}]

        # Append user or assistant messages based on whether it's a bot message
        for message in messages:
            try:
                role = "assistant" if message.get("subtype") == "bot_message" else "user"
                text = message.get("text", "")
                chat_array.append({"role": role, "content": text})
            except Exception as e:
                logging.error(f"Error processing message: {e}")

        return chat_array