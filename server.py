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
app = Flask(__name__)
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
bolt_app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
handler = SlackRequestHandler(bolt_app)

# @bolt_app.event("message")
# def handle_message_events(body, logger):
#     logger.info(body)

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

@bolt_app.message("131bot, make a form")
def make_form(payload, say):
    create_new_form.create_form("my test form2", "testytesty", [], get_token.get_token())

@bolt_app.message(re.compile("131bot, get me all responses for the form with id (.*) for question (.*)"))
def trigger_form(payload, say):
    regex = re.compile("id (.*) for question (.*)")
    (form_id, question_body) = regex.findall(payload["text"])[0]
    res = read_form.read_form(form_id, question_body, get_token.get_token())
    say(f'ok! here are the responses {res}')

@app.route("/131bot/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)