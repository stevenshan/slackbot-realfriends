import os

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