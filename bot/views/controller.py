import os
import flask
from urllib.parse import quote as urlencode
import requests

from bot.views import message, latex, file, sandbox

# create blueprint to register routes to
views = flask.Blueprint("app", __name__)

SCOPES = " ".join([
    "channels:history",
    "groups:history",
    "im:history",
    "mpim:history",
    "bot",
    "commands"
])

REDIRECT_URI = urlencode("https://realfriends-slack-bot.herokuapp.com/ready")

@views.route("/", methods=("GET",))
def index_get():
    clientID = os.environ.get("CLIENT_ID", "")
    return flask.redirect(
        "https://slack.com/oauth/authorize?client_id=%s&scope=%s&redirect_uri=%s" % 
        (clientID, SCOPES, REDIRECT_URI)
    ) 

@views.route("/ready", methods=("GET", "POST"))
def ready():
    return "ok"

@views.route("/", methods=("POST",))
def index_post():
    # return challenge
    data = flask.request.get_json()

    if data is None:
        return "hi"

    if data.get("type") == "url_verification":
        return flask.jsonify({
            "challenge": str(data.get("challenge", ""))
        })


    if data.get("type") == "event_callback":
        event = data.get("event", {})
        if event.get("type") == "message":
            return message.message(data)

    return "nothing to see here"

def argParse(text):
    parts = text.split()
    preview = False
    if len(parts) == 0:
        raise ValueError("rip")
    elif parts[0] == "preview":
        preview = True
        text = " ".join(parts[1:])

    return preview, text

@views.route("/slash", methods=("POST",))
def slash():
    command = flask.request.values.get("command", "")
    text = flask.request.values.get("text", "")
    user = flask.request.values.get("user_id", "")
    responseURL = flask.request.values.get("response_url")

    if text.strip(" ") == "":
        return "no text received"

    if command == "/math":
        preview, text_ = argParse(text)

        image_url = latex.getLatexURL(text_)
        data = {
            "attachments": [
                {
                    "text": ("*<@%s>*: %s" % (user, text_)),
                    "image_url": image_url
                }
            ]
        }

        if not preview:
            data["response_type"] = "in_channel"
            requests.post(responseURL, json=data)
            return ""

        return flask.jsonify(data)
    elif command == "/python":
        preview, text_ = argParse(text)

        result = sandbox.execute(text)

        image_url = latex.getLatexURL(text_)
        if str(result) == "":
            text = "<@%s>: ```%s```" % (user, result)
        else:
            text = "<@%s>: Empty Response" % user

        data = {"text": text}

        if not preview:
            data["response_type"] = "in_channel"
            requests.post(responseURL, json=data)
            return ""

        return flask.jsonify(data)

    return "unrecognized command '%s'" % command
