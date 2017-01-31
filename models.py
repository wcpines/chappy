import datetime
from app import db
from peewee import (Model, SqliteDatabase, CharField,
                    DateTimeField, ForeignKeyField, TextField)


# base model for specifying DB, and any shared methods/behaviors.
# this information is not

class BaseModel(Model):
    # datetime.datetime object in UTC. TZ-naive object, so localize provides this.
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    class Meta:
        database = db

class Message(BaseModel):
    user_id = ForeignKeyField(User)
    channel_id = ForeignKeyField(Channel)
    text_content = TextField()
    img_url = TextField(null=True) # metadata to be retreived via emebedly, client-side
    video_url = TextField(null=True) #

    def __repr__(self):
        return (
            f"Message("
            f"id={self.id!r}, "
            f"text_content={self.text_content!r}, "
            f"img_url={self.img_url!r}, "
            f"video_url={self.video_url!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('-created_at',)


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField()
    password = CharField()


    def __repr__(self):
        return (
            f"User("
            f"id={self.id!r}, "
            f"email={self.email!r}, "
            f"password={self.password!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('-created_at',)

class Channel(BaseModel):


    def __repr__(self):
        return (
            f"Channel("
            f"id={self.id!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )


    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('sender_id', 'recipient_id'), True),
        )


class ChannelUser(BaseModel):
    user_id = ForeignKeyField(User)
    channel_id = ForeignKeyField(Channel))

    class Meta:
        indexes = (
            (('user_id', 'channel_id'), True),
        )





(channel ~= conversation)

#  channel has many users (sender(s) and recipient(s))
#  channel has many messages

#  message belongs to a sender
#  message belongs to a channel
#  message has at least 1 recipient

#  user has many conversations
#  sender-user sends many messages
#  recipient-user receives many messages
