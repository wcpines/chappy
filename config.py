import os

class BaseConfig(object):
    FLASK_SECRET_KEY_BASE=os.environ['FLASK_SECRET_KEY_BASE']
    SECRET_KEY=os.environ['SECRET_KEY']
    DATABASE=os.environ['CONNECTION_URL'] # export CONNECTION_URL='chappy.db'
    BCRYPT_LOG_ROUNDS = 10 # enough for reasonable security, but not slow

class DevConfig(BaseConfig):
    DEBUG=True

class ProdConfig(BaseConfig):
    DEBUG=False

