import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from forms import authentication
from slack_bolt.adapter.flask import SlackRequestHandler
from google_auth_oauthlib.flow import InstalledAppFlow
from forms import get_token
import re
import flask
from forms import read_form
from forms import create_new_form
from messages import message_sender
from messages import slack_utils

app = Flask(__name__)
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
bolt_app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
handler = SlackRequestHandler(bolt_app)

SCOPES = ["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/forms.responses.readonly"]
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES, redirect_uri="https://rat-relaxing-briefly.ngrok-free.app/131bot/authorize")


@app.route("/131bot/authorize")
def finish_auth():
    url = flask.request.url.replace("http", "https")
    flow.fetch_token(authorization_response=url)
    creds = flow.credentials
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())
    return "complete! you can return to slack now :P"
    

@bolt_app.message("authorize")
def start_auth(payload, say):
    auth_url, _ = flow.authorization_url(prompt="consent")
    say(f"go to this link to authorize: {auth_url}")

@bolt_app.message("hello 131bot")
def say_hello(payload, say):
    say("hello there")

@bolt_app.message("131bot, say (.*) to (.*)")
def send_it(payload, say):
    regex = re.compile("say (.*) to (.*)")
    (message, user_name) = regex.findall(payload["text"])[0]
    status = message_sender.send_message(bolt_app, user_name, message)
    say("sent!" if status else "an error occurred")

@bolt_app.message("131bot, make an attendance form for (.*)")
def make_form(payload, say):
    regex = re.compile("for (.*)")
    (event_name) = regex.findall(payload["text"])[0]
    questions = {
                    "title": (
                        "Your preferred full name"
                    ),
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            },
                        }
                    },
                }
    create_new_form.create_form(f"{event_name} Attendance", "", questions, get_token.get_token())

@bolt_app.message(re.compile("131bot, get me all responses for the form with id (.*) for question (.*)"))
def trigger_form(payload, say):
    regex = re.compile("id (.*) for question (.*)")
    (form_id, question_body) = regex.findall(payload["text"])[0]
    res = read_form.read_form(form_id, question_body, get_token.get_token())
    say(f'ok! here are the responses {res}')
    say(f'you are missing {read_form.compare_with_roster(res)}')

@bolt_app.message(re.compile("131bot, send an alert form with id (.*) with text (.*)"))
def search(payload, say):
    regex = re.compile("id (.*) with text (.*)")
    (form_id, text_body) = regex.findall(payload["text"])[0]
    question_body = "Your preferred full name"
    res = read_form.read_form(form_id, question_body, get_token.get_token())
    unanswereds = read_form.compare_with_roster(res)
    fails = message_sender.batch_send_message(bolt_app, unanswereds, text_body)
    msg = "all good!" if len(fails) == 0 else f'messages have been sent, the following didnt work: {fails}'
    say(msg)

@bolt_app.message("131bot, send alert to people without profile pictures")
def send_alert(payload, say):
    anons = slack_utils.check_all_users_profile_pictures(bolt_app)
    fails = message_sender.batch_send_message(bolt_app, anons, "Please make sure to set a Slack profile picture. It is very important so that we can see who you are!")
    msg = "all good!" if len(fails) == 0 else f'messages have been sent, the following didnt work: {fails}'
    say(msg)

@app.route("/131bot/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)