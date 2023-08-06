from pygyver.etl.toolkit import get_env_var
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackMessenger():

    def __init__(self, bot):
        self.access_token = get_env_var("SLACK_BOT_"+bot.upper())

    def send_message(self, channel_id, text):

        client = WebClient(self.access_token)

        try:
            # Call the conversations.list method using the WebClient
            result = client.chat_postMessage(
                channel=channel_id,
                text=text
            )
            print(result)
        except SlackApiError as slack_error:
            raise Exception(f"SLACK FAILED TO SEND TEXT: '{text}' TO CHANNEL: '{channel_id}'") from slack_error
