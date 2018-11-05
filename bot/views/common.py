import os
import requests

def get(dictionary, *keys):
    try:
        for key in keys:
            dictionary = dictionary[key]
        return dictionary
    except (KeyError, TypeError):
        return None

def getToken(bot=False):
    if bot:
        return os.environ.get("BOT_ACCESS_TOKEN")
    else:
        return os.environ.get("ACCESS_TOKEN")

POST_MESG = "https://slack.com/api/chat.postMessage"

def postMessage(channel, text):
    requests.post(POST_MESG, data={
        "token": getToken(bot=True),
        "channel": channel,
        "text": text
    })

def argParse(text):
    parts = text.split()
    preview = False
    if len(parts) == 0:
        raise ValueError("rip")
    elif parts[0] == "preview":
        preview = True
        text = " ".join(parts[1:])

    return preview, text

def execute(interpreter, text, user, parse=True):
    if parse:
        preview, text_ = argParse(text)
    else:
        preview, text_ = False, text

    result = interpreter.execute(text_)

    try:
        label_ = interpreter.__name__
        i = label_.rfind(".") + 1
        label = str(label_[i:]).capitalize()
    except:
        label = ""

    if str(result) == "":
        header = "<@%s>: %s -- `%s`" % (user, label, text_)
        body = "_Empty Response_"
    else:
        header = "<@%s>: %s -- `%s`" % (user, label, text_)
        body = "```%s```" % result

    data = {
        "text": header,
        "attachments": [
            {
                "text": body
            }
        ]
    }

    if not preview:
        data["response_type"] = "in_channel"

    return preview, data

