"""
events for when a file is created or modified
"""

import requests

from bot.views import sandbox, common

FILE_INFO_URL = "https://slack.com/api/files.info"

def getFile(id):

    try:
        _file = requests.post(FILE_INFO_URL, data={
            "token": common.getToken(),
            "file": id
        }).json()

        if _file.get("ok"):
            return _file["file"]
    except:
        pass

    return None

def created(data, as_file = False):

    if as_file:
        file = data
    else:
        file = getFile(common.get(data, "event", "file_id"))

    if common.get(file, "filetype") == "python":
        download = common.get(file, "url_private")
        if download is None or download.strip(" ") == "":
            return None

        try:
            _content = requests.get(download, headers={
                "Authorization": "Bearer %s" % common.getToken()
            })
        except:
            return None

        if _content.status_code != 200:
            return None

        content = _content.text

        result = sandbox.execute(content)
        result = str(result).strip("\n")

        return result 

    return None