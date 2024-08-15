from requests import get, post
import os

def get_all_users():
    url = "https://slack.com/api/users.identity"
    user_list_response = get(url, headers={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"})
    print (user_list_response.content)
def find_user_channel(user):
    # POST https://slack.com/api/conversations.open
    print()

get_all_users()