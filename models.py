import datetime
from peewee import (Model, SqliteDatabase, CharField,
                    DateTimeField, ForeignKeyField, TextField)


DATABASE = 'chappy.db'

db = SqliteDatabase(DATABASE)

# base model for specifying DB, and any shared methods/behaviors.
class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        database = db

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()

    class Meta:
        order_by = ('username',)

class Conversation(BaseModel):
    sender_user = ForeignKeyField(User, related_name='conversations')
    recipient_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on sender/recipient user.
            (('sender_user', 'recipient_user'), True),
        )

class Message(BaseModel):
    user = ForeignKeyField(User)
    text_content = TextField()
    img_url = TextField()
    #  img_data
    video_url = TextField()
    #  video_data
    pub_date = DateTimeField()

    class Meta:
        order_by = ('-pub_date',)
