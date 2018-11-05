"""
when a message is received or changed
"""

from bot.views import common, file
import requests
from base64 import b64encode, b64decode

def decode(base64):
    return b64decode(base64.encode("ascii")).decode("ascii")

trigger = decode("RnVja1N0ZXZlbigpOw==")
responseWord = decode("ZnVjaw==")

def message(data):
    subtype = common.get(data, "event", "subtype")
    channel = common.get(data, "event", "channel")
    user = common.get(data, "event", "user")

    if subtype == "file_share":
        result = file.created(data["event"]["files"][0], as_file=True)

        if result is not None:
            language, result = result
            if str(result) == "":
                text = "<@%s>: %s\n_Empty Response_" % (user, language)
            else:
                text = "<@%s>: %s ```%s```" % (user, language, result)

            common.postMessage(channel, text)
    elif common.get(data, "event", "text").strip(" ") == trigger:
        entity = user
        if entity is None or entity == "":
            entity = str(common.get(data, "event", "username"))
        common.postMessage(channel,
            "No %s you <@%s>" % (responseWord, entity))

    return ""
