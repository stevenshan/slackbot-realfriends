"""
when a message is received or changed
"""

from bot.views import common, file
import requests

def message(data):
    subtype = common.get(data, "event", "subtype")

    if subtype == "file_share":
        result = file.created(data["event"]["files"][0], as_file=True)

        if result is not None:
            user = str(common.get(data, "event", "user"))

            if str(result) == "":
                text = "<@%s>: _Empty Response_" % user
            else:
                text = "<@%s>: ```%s```" % (user, result)

            common.postMessage(common.get(data, "event", "channel"), text)

    return ""
