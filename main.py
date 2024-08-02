import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ.get('SLACK_BOT_TOKEN')
client = WebClient(token = slack_token)

try:
    client.chat_postMessage(channel="slackbot-test", text="no way")
    
except SlackApiError as e:
    print(e)