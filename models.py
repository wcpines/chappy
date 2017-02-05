from app import db
from peewee import Model, SqliteDatabase, CharField, DateTimeField, ForeignKeyField, TextField
from playhouse.fields import PasswordField
import datetime


# base model for specifying DB, and any shared methods/behaviors.
# this information is not

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    class Meta:
        database = db


# BaseUser should give me set_password and check_password methods
class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    phone = CharField(null=True)
    password = PasswordField()
    #  password = CharField()

    def __repr__(self):
        return (
            f"User("
            f"id={self.id!r}, "
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"phone={self.phone!r}, "
            f"password={self.password!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('-created_at',)


class Channel(BaseModel):
    title = CharField()

    def __repr__(self):
        return (
            f"Channel("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('-created_at',)


class Message(BaseModel):
    user_id = ForeignKeyField(User)
    channel_id = ForeignKeyField(Channel)
    text_content = TextField()
    img_url = TextField(null=True) # client to retreive metadata via emebedly
    video_url = TextField(null=True) #

    def __repr__(self):
        return (
            f"Message("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"channel_id={self.channel_id!r}, "
            f"text_content={self.text_content!r}, "
            f"img_url={self.img_url!r}, "
            f"video_url={self.video_url!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('-created_at',)


class ChannelUser(BaseModel):
    user_id = ForeignKeyField(User)
    channel_id = ForeignKeyField(Channel)

    def __repr__(self):
        return (
            f"ChannelUser("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"channel_id={self.channel_id!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('-created_at',)
