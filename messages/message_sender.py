from messages import get_channel
import json
import time

def batch_send_message(bolt_app, users_names, message):
    fails = []
    for user in users_names:
        status = send_message(bolt_app, user, f"Hello {user}! {message} (P.S. this is an automated message. if you think this message wasn't meant for you, let Vicky know!!)")
        if not status:
            fails.append(user)
        time.sleep(5)
    return fails 

def send_message(bolt_app, user_name, message):
    aliases = json.load(open("known_aliases.json"))
    user_name = aliases[user_name] if user_name in aliases else user_name
    id = get_channel.get_user_id(bolt_app, user_name)
    time.sleep(1)
    if id == None:
        return False
    status = bolt_app.client.chat_postMessage(channel=id, text=message)
    return status['ok']