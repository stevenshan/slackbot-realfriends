from urllib.parse import quote as urlencode
import requests

LATEX = "http://latex.codecogs.com/png.latex?%5Cdpi%7B300%7D%20"

def getLatexURL(text):
    return LATEX + urlencode(text)
