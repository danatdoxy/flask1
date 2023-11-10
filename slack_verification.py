import secrets
import hashlib
import hmac
import time
import logging

# def logging_setup():
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     return logger
# Function to verify the signature of the incoming Slack request
def verify_slack_signature(slack_signing_secret, request_data):
    """
    Verify the signature of a Slack request using the provided signing secret.

    Args:
        slack_signing_secret (str): The signing secret provided by Slack.
        request_data (dict): The data of the incoming request.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    # Retrieve the signature and timestamp from the incoming request's headers
    slack_signature = request_data.get('signature')
    slack_request_timestamp = request_data.get('timestamp')
    print('Verifying slack signature')

    # Convert timestamp to int and check if the timestamp is within five minutes of the server's current time
    if abs(time.time() - int(slack_request_timestamp)) > 60 * 5:
        return False

    # Retrieve the raw body of the request for forming the basestring
    request_body = request_data.get('body')

    # Form the basestring as stated by Slack documentation
    VERSION = 'v0'
    sig_basestring = ''.join([VERSION, slack_request_timestamp, request_body]).encode('utf-8')
    print('generating hash')
    # Hash the basestring using the signing secret
    my_signature = f"{VERSION}=" + hmac.new(slack_signing_secret.encode('utf-8'), sig_basestring, hashlib.sha256).hexdigest()
    print('comparing signatures')
    # Compare the computed signature with the signature on the request using a constant time comparison function
    return secrets.compare_digest(my_signature, slack_signature)
