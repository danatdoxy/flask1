import secrets
import hashlib
import hmac
import time
import logging
import sys
from my_classes import SlackRequestData
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def verify_slack_signature(slack_signing_secret, request_data, body):
    """
    Verify the signature of a Slack request using the provided signing secret.

    Args:
        slack_signing_secret (str): The signing secret provided by Slack.
        request_data (dict): The data of the incoming request.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    # Retrieve the signature and timestamp from the incoming request's headers
    slack_signature = request_data.signature
    slack_request_timestamp = request_data.timestamp
    logging.info('Verifying slack signature')

    # Convert timestamp to int and check if the timestamp is within five minutes of the server's current time
    if abs(time.time() - int(slack_request_timestamp)) > 60 * 5:
        return False

    # # Retrieve the raw body of the request for forming the basestring
    # body = request_data.get('body')

    # Form the basestring as stated by Slack documentation
    VERSION = 'v0'
    sig_basestring = ':'.join([VERSION, slack_request_timestamp, body]).encode('utf-8')
    logging.info('generating hash')
    # Hash the basestring using the signing secret
    my_signature = f"{VERSION}=" + hmac.new(slack_signing_secret.encode('utf-8'), sig_basestring, hashlib.sha256).hexdigest()
    logging.info('comparing signatures')
    # Compare the computed signature with the signature on the request using a constant time comparison function
    return secrets.compare_digest(my_signature, slack_signature)
