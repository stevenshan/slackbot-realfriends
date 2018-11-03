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
                header = "<@%s>:" % user
                body = "_Empty Response_"
            else:
                header = "<@%s>:" % user
                body = "```%s```" % result

            requests.post(common.POST_MESG, data={
                "token": common.getToken(bot=True),
                "channel": common.get(data, "event", "channel"),
                "text": header,
                "attachments": [
                    {
                        "text": body 
                    }
                ] 
            })

    return ""
