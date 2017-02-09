import datetime
from chappy.db import db
from playhouse.fields import PasswordField
from peewee import Model, SqliteDatabase, CharField, DateTimeField,\
        ForeignKeyField, TextField, IntegerField


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    class Meta:
        database = db


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
        order_by = ('created_at',)


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
        order_by = ('created_at',)


class Message(BaseModel):
    user = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)
    text_content = TextField()
    img_url = CharField(null=True) # retreive metadata via emebedly before save
    img_html = TextField(null=True)
    img_height = IntegerField(null=True)
    img_width = IntegerField(null=True)
    video_url = CharField(null=True) #
    video_html = TextField(null=True)
    video_source = CharField(null=True) #
    video_length = IntegerField(null=True) #

    def __repr__(self):
        return (
            f"Message("
            f"id={self.id!r}, "
            f"user_id={self.user.id!r}, "
            f"channel_id={self.channel.id!r}, "
            f"text_content={self.text_content!r}, "
            f"img_url={self.img_url!r}, "
            f"img_height={self.img_height!r}, "
            f"img_width={self.img_width!r}, "
            f"video_url={self.video_url!r}, "
            f"video_source={self.video_source!r}, "
            f"video_length={self.video_length!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('created_at',)


class ChannelUser(BaseModel):
    # NOTE: peewee stores the whole object, not just the key/id
    user = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)

    def __repr__(self):
        return (
            f"ChannelUser("
            f"id={self.id!r}, "
            f"user_id={self.user.id!r}, "
            f"channel_id={self.channel.id!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"updated_at={self.updated_at:%Y-%m-%d %H:%M:%S})"
        )

    class Meta:
        order_by = ('created_at',)


def init_db():
    db.connect()

    #  NOTE: Testing purposes only!
    ################################################################
    ################################################################
    tables = [User, Channel, Message, ChannelUser]
    for table in tables:
        try:
            db.drop_table(table)
        except Exception as e:
            print("Failed to drop {}; {}".format(table, e.args[0]))
    ################################################################
    ################################################################

    db.create_tables(tables, safe=True)

