import os

from flask import Flask, g, redirect, request, session, url_for, abort, jsonify
from flask_socketio import SocketIO, send, emit
import flask_jwt_extended as fj
import jwt as jt # see FIXME below
import peewee
from playhouse.fields import PasswordField

from chappy.config import Config
from chappy.models import User, Channel, ChannelUser, Message, init_db

from adapters.embedly_adapter import get_video_metadata, get_img_metadata
from adapters.twilio_adapter import message_user


app = Flask(__name__)
app.config.from_object(Config)

jwt = fj.JWTManager(app)
socketio = SocketIO(app)

###################
# JWT SESSION SETUP
###################

# FIXME: fj.get_jwt_identity appears to be borked; I wrote my own:

def decode_identity():
    algorithm = fj.config.__dict__['ALGORITHM']
    secret = app.config.get('SECRET_KEY')
    token = request.headers.get('AUTHORIZATION').split(' ')[1]
    identity = jt.decode(token, secret, algorithm)
    return identity['identity']


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 101,
        'log_message': 'JWT token has expired'
    }), 200


##################################
# App routes and conroller actions
##################################

@app.route('/signup', methods=['POST'])
def signup():
    try:
        user = User.create(
            username = request.get_json().get('username'),
            email = request.get_json().get('email'),
            phone = request.get_json().get('phone'),
            password = request.get_json().get('password') # supposedly encrypted by PasswordField
        )

        jwt = {'access_token': fj.create_access_token(identity=user.id)}
        return jsonify(jwt), 200

    except Exception as e:
        #  return jsonify({"log_message": "{} already in use".format(e.args[0].split(".")[-1])})
        print(e)
        return jsonify({"log_message": "Error! " " :( " "Check application logs"}), 400


@app.route('/login', methods=['POST'])
def login():
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    user = User.get(User.email == email)

    if user and user.password.check_password(password): # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#PasswordField
        jwt = {'access_token': fj.create_access_token(identity=user.id)}
        return jsonify(jwt), 200
    else:
        return jsonify({"log_message": "Bad username or password"}), 401

@fj.jwt_required
@app.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if user_id != decode_identity():
        return jsonify({"log_message": "Unauthorized user"})
    else:
        edit_user_query = (
            User
            .update(
                username=request.get_json().get('username') or User.username,
                email=request.get_json().get('email') or User.email,
                phone=request.get_json().get('phone')
            )
            .where(User.id == user_id)
        )
        edit_user_query.execute()
        edited_user = User.get(User.id == user_id)
        return jsonify({'username': edited_user.username, 'email': edited_user.email, 'phone': edited_user.phone})


# creating a conversation *requires* two users, inviter and invitee
@fj.jwt_required
@app.route('/channels', methods=['POST'])
def create_channel():
    user_id = decode_identity()

    title = request.get_json().get('title')
    channel_invitee_id = request.get_json().get('channelInviteeId')
    channel = Channel.create(title=title)
    ChannelUser.get_or_create(user_id=channel_invitee_id, channel_id=channel.id)
    ChannelUser.get_or_create(user_id=user_id, channel_id=channel.id)
    return jsonify({"log_message": f"Successfully created channel {channel.id!r}"})


@fj.jwt_required
@app.route('/channels/<int:channel_id>', methods=['GET'])
def fetch_channel_participants(channel_id):
    channel_users = (
        ChannelUser
        .select(ChannelUser, User)
        .join(User)
        .where(ChannelUser.channel_id == channel_id)
    )
    users = [cu.user for cu in channel_users]

    return jsonify(
        [{'username': user.username, 'email': user.email} for user in users]
    )

@fj.jwt_required
@app.route('/channels/<int:channel_id>', methods=['POST', 'DELETE'])
def join_or_leave_channel(channel_id):
    user_id = decode_identity()

    username = User.get(User.id == user_id).username
    if request.method == 'POST':
        ChannelUser.get_or_create(user_id=user_id, channel_id=channel_id)
        return jsonify({"log_message": f"{username!r} successfully joined channel", "channelId": channel_id})
    else: # DELETE
        delete_channel_users = ChannelUser.delete().where(
            ChannelUser.channel_id == channel_id and
            ChannelUser.user_id == user_id
        )
        delete_channel_users.execute()

        return jsonify({"log_message": f"{username!r} successfully left channel {channel_id!r}"})

# corresponding realtime events, would be provided via js client
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)



@fj.jwt_required
@app.route('/channels/<int:channel_id>/messages', methods=['GET'])
def fetch_messages_from_channel(channel_id, offset=1, limit=50):
    user_id = decode_identity()

    messages = Message.select().where(Message.channel_id == channel_id).paginate(offset, limit)
    return jsonify([message._data for message in messages])


@fj.jwt_required
@app.route('/channels/<int:channel_id>/messages', methods=['POST'])
def send_message_to_channel(channel_id):
    """
    If the message has a video URL included, use embedly adapter to fetch
    metadata to include on the object, and ignore any image URL.  If image
    url present, do the opposite
    """
    user_id = decode_identity()

    video_url = request.get_json().get('videoUrl')
    img_url = request.get_json().get('imgUrl')

    if video_url:
        video_data = get_video_metadata(video_url)

        new_message = Message.create(
            channel_id=channel_id,
            user_id=user_id,
            text_content=request.get_json().get('textContent'),
            video_url=video_url,
            video_html=video_data.get('html'),
            video_source=video_data.get('source'),
            video_length=video_data.get('length'),
        )

    elif img_url and not video_url:
        img_data = get_img_metadata(img_url)

        new_message = Message.create(
            channel_id=channel_id,
            user_id=user_id,
            text_content=request.get_json().get('textContent'),
            img_url=img_url,
            img_html=img_data.get('html'),
            img_height=img_data.get('height'),
            img_width=img_data.get('width'),
        )
    else:
        new_message = Message.create(
            channel_id=channel_id,
            user_id=user_id,
            text_content=request.get_json().get('textContent'),
        )

    socketio.emit('message', new_message._data, room=channel_id, include_self=True)

    return jsonify(new_message._data)

@fj.jwt_required
@app.route('/channels/<int:channel_id>/messages/<int:message_id>', methods=['PUT', 'DELETE'])
def edit_or_delete_message_from_channel(channel_id,message_id):
    user_id = decode_identity()

    if request.method == 'PUT':
        edit_message_query = (
            Message
            .update(
                text_content=request.get_json().get('textContent') or Message.text_content,
                img_url=request.get_json().get('imgUrl') or Message.img_url,
                video_url=request.get_json().get('videoUrl') or Message.video_url
            )
            .where(Message.id == message_id and Message.channel_id == channel_id)
        )
        edit_message_query.execute()

        edited_message = Message.get(Message.id == message_id and Message.channel_id == channel_id)
        return jsonify(edited_message._data)

    else: # DELETE
        Message.get(Message.id == message_id).delete_instance()
        return jsonify({"log_message": f"Successfully deleted message {message_id!r}"})

if __name__ == '__main__':
    from IPython import embed
    init_db()
    #  app.run(debug=Config.DEBUG)
    socketio.run(app,debug=Config.DEBUG)
