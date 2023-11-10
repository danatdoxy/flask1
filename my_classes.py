class SlackRequestData:
    def __init__(self, form, headers):
        self.timestamp = headers.get('X-Slack-Request-Timestamp')
        self.signature = headers.get('X-Slack-Signature')
        self.response_url = form.get('response_url')
        self.text = form.get('text')
        self.command = form.get('command')
        self.user_id = form.get('user_id')
        self.channel_id = form.get('channel_id')
        self.channel_name = form.get('channel_name')
        self.team_id = form.get('team_id')
        self.trigger_id = form.get('trigger_id')
        self.token = form.get('token')

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