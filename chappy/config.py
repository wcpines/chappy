import os

class Config(object):
    FLASK_SECRET_KEY_BASE=os.getenv('FLASK_SECRET_KEY_BASE')
    SECRET_KEY=os.getenv('SECRET_KEY', 'something_secret_for_dev')
    DATABASE=os.getenv('CONNECTION_URL', 'chappy.db')
    EMBEDLY_API_KEY = os.getenv('EMBEDLY_API_KEY')
    #  TWILIO_SID = os.getenv('TWILIO_SID')
    #  TWILIO_API_KEY = os.getenv('TWILIO_API_KEY')
    #  TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
    DEBUG = os.getenv("DEBUG", True)
