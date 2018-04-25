"""
The config class to store all the configs
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # this variable is used to avoid Cross-Site Request Forgery
    # or CSRF attack through forms
    SECRET_KEY = os.environ.get("SECRET_KEY") or "freshslice"

    # to set the specific DATABASE URL by envirenmental variable
    SQLALCHEMY_DATABASE_URI= os.environ.get("DATABASE_URL") or \
            "sqlite:////" + os.path.join(basedir,"app.db")

    SQLALCHEMY_TRACK_MODIFICATION = False
