"""
when a message is received or changed
"""

from bot.views import common, file
import requests

def message(data):
    subtype = common.get(data, "event", "subtype")

    if subtype == "file_share":
        result = file.created(data["event"]["files"][0], as_file=True)

        user = str(common.get(data, "event", "user"))

        requests.post(common.POST_MESG, data={
            "token": common.getToken(bot=True),
            "channel": common.get(data, "event", "channel"),
            "text": "<@%s>: ```%s```" % (user, result)
        })

    return "test"