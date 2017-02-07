import os

class Config(object):
    FLASK_SECRET_KEY_BASE=os.environ['FLASK_SECRET_KEY_BASE']
    SECRET_KEY=os.environ['SECRET_KEY']
    DATABASE=os.environ['CONNECTION_URL'] # export CONNECTION_URL='chappy.db'
    EMBEDLY_API_KEY = os.environ['EMBEDLY_API_KEY']
    TWILIO_SID = os.environ['TWILIO_SID']
    TWILIO_API_KEY = os.environ['TWILIO_API_KEY']
    TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
    DEBUG = os.environ.get("DEBUG", True)
