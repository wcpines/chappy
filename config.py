class BaseConfig(object):
    DEBUG=True
    SECRET_KEY=os.environ['SECRET_KEY']
    DATABASE=os.environ['CONNECTION_URL']
