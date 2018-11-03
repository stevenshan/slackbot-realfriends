import flask
from bot.views import message, latex

# create blueprint to register routes to
views = flask.Blueprint("app", __name__)

@views.route("/", methods=("GET",))
def index_get():
    return "hi"

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
                    "image_url": image_url
                }
            ]
        }

        if not preview:
            data["response_type"] = "in_channel"

        return flask.jsonify(data)

    return "unrecognized command '%s'" % command
