import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
import re

from forms import read_form
app = Flask(__name__)
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
bolt_app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
handler = SlackRequestHandler(bolt_app)

@bolt_app.message("hello 131bot")
def say_hello(payload, say):
    say("hello there")

@bolt_app.message("131bot, get me all responses for the form with id 1AHGp3LEh0W5LncNSh3TNFkYkKesz9iHzHJ1HNjmEg1g")
def trigger_form(payload, say):
    print(payload["text"])
    regex = re.compile("id (.*)")
    form_id = regex.findall(payload["text"])[0]
    print(form_id)
    res = read_form.read_form(form_id)
    say(f'ok! here are the responses {res}')

@app.route("/131bot/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)