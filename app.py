from flask import Flask, g, redirect, request, session, url_for, abort, jsonify
from flask.ext.login import LoginManager, UserMixin, login_required
#  from helpers import issue_token, before_request, after, login_required
from flask_socketio import SocketIO, send, emit
from peewee import SqliteDatabase
from IPython import embed
import os

from pytz import timezone

#  EST = timezone('US/Eastern')
#  UTC = timezone('UTC')

app = Flask(__name__)

# toggle between development/production using env var
app.config.from_object(os.environ['APP_SETTINGS']) # config.DevConfig
db = SqliteDatabase(app.config['DATABASE'], threadlocals=True)

login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app)

# import after db/config setup
from models import *


def init_db():
    db.connect()
    db.create_tables([User, Channel, Message, ChannelUser], safe=True)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'This would normally render a SPA homepage(?)'})


# creating a conversation *requires* two users, inviter and invitee
@app.route('/channels', methods=['POST'])
def create_channel():
    #  user_id = request.get_json().get('user_id') # FIXME: how front-end passes the id
    title = request.get_json().get('title')
    channel_invitee_id = request.get_json().get('channelInviteeId')
    channel = Channel.create(title=title).save()
    ChannelUser.get_or_create(user_id=channel_invitee_id, channel_id=channel.id)
    ChannelUser.get_or_create(user_id=user_id, channel_id=channel.id)
    return jsonify({"log_message": f"Successfully left channel {channel_id!r}"})

@app.route('/channels/<int:channel_id>', methods=['GET'])
def get_channel_participants(channel_id):
    channel_users = ChannelUser.select(ChannelUser.channel_id == channel_id)
    #  e.g. ChannelUser(id=1, user_id=1, channel_id=1)
    user_ids = [user_id.user_id for user_id in channel_users]
    users = User.select(User.id << user_ids)
    return jsonify(users) # <= return an array of user objects

@app.route('/channels/<int:channel_id>', methods=['POST', 'DELETE'])
def join_or_leave_channel(channel_id):
    embed()
    #  user_id = request.get_json().get('user_id') # FIXME: how front-end passes the id
    if request.method == 'POST':
        ChannelUser.get_or_create(user_id=user_id, channel_id=channel_id)
        return jsonify({"log_message": f"Successfully joined channel{channel_id!r}"})
    else: # DELETE
        channel_users = ChannelUser.select().where(
            ChannelUser.channel_id == channel_id and
            ChannelUser.user_id == user_id
        ).delete_instance()
        return jsonify({"log_message": f"Successfully left channel {channel_id!r}"})

@app.route('channel/<int:channel_id>/messages/'), methods=['GET', 'POST'])
def fetch_or_send_to_channel(channel_id):
    #  user_id = request.get_json().get('user_id') # FIXME: how front-end passes the id
    if request.method == 'GET':
        messages = Message.select().where(Message.channel_id == channel_id)
        return jsonify(messages)
    else: #POST
        request_json = request.get_json()
        new_message = Message.create(
            channel_id=channel_id,
            user_id=user_id,
            text_content=request_json.get('textContent'),
            img_url=request_json.get('imgUrl'),
            video_url=request_json.get('videoUrl')
        ).save
        return jsonify(new_message)

@app.route('channel/<int:channel_id>/messages/<int:message_id>', method=['PUT', 'DELETE'])
def edit_or_delete_message(message_id):
    if request.method == 'PUT':
        edited_message = Message.get(Message.id == message_id)
        edit_message_query = Message.update(
            text_content=request_json.get('textContent'),
            img_url=request_json.get('imgUrl'),
            video_url=request_json.get('videoUrl')
        ).where(Message.id == message_id)
        edit_message_query.execute()
        return jsonify(new_message)
    else: # DELETE
        message = Message.get(Message.id == message_id)
        message.delete_instance()
        return jsonify({"log_message": f"Successfully deleted message {message_id!r}"})


# allow running from the command line
if __name__ == '__main__':
    init_db()
    app.run()
    #  socketio.run(app)



#  TODO (goals):
    #  - Assign written message to a user, and message can be sent to a receiver
    #   (based on ID specified? Based on join object/relation?)
    #  - create users, authenticate users
    #  - write and retrieve over a socket connection



