import hashlib
import hmac
import time

# Function to verify the signature of the incoming Slack request
def verify_slack_signature(slack_signing_secret, request_data):
    # Retrieve the signature and timestamp from the incoming request's headers
    slack_signature = request_data.signature
    slack_request_timestamp = request_data.timestamp

    # Convert timestamp to int and check if the timestamp is within five minutes of the server's current time
    if abs(time.time() - int(slack_request_timestamp)) > 60 * 5:
        return False

    # Retrieve the raw body of the request for forming the basestring
    request_body = request_data.to_dict()

    # Form the basestring as stated by Slack documentation
    sig_basestring = f"v0:{slack_request_timestamp}:{request_body}".encode('utf-8')

    # Hash the basestring using the signing secret
    my_signature = 'v0=' + hmac.new(slack_signing_secret.encode('utf-8'), sig_basestring, hashlib.sha256).hexdigest()

    # Compare the computed signature with the signature on the request
    return hmac.compare_digest(my_signature, slack_signature)
