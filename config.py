import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    pass

"""
Import configuration variables from system environment variables
"""

Config.SECRET_KEY = os.environ.get("SECRET_KEY", "######")
