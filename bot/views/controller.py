import os
import flask
from bot.views import message, latex
from urllib.parse import quote as urlencode
import requests

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


    if (data.get("type") == "event_callback" and
            data.get("event", {}).get("type") == "message"):
        return message.message(data)

    return "nothing to see here"

@views.route("/slash", methods=("POST",))
def slash():
    command = flask.request.values.get("command", "")
    text = flask.request.values.get("text", "")
    user = flask.request.values.get("user_id", "")
    responseURL = flask.request.values.get("response_url")

    if text.strip(" ") == "":
        return "no text received"

    if command == "/math":
        parts = text.split()
        preview = False
        text_ = text
        if len(parts) == 0:
            return "rip"
        elif parts[0] == "preview":
            preview = True
            text_ = " ".join(parts[1:])

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

    return "unrecognized command '%s'" % command
