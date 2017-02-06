import peewee
from chappy.config import Config

db = peewee.SqliteDatabase(Config.DATABASE, threadlocals=True)
