import os

from flask import Flask, g, redirect, request, session, url_for, abort, jsonify
from flask_socketio import SocketIO, send, emit
import flask_jwt_extended as fj
import jwt as jt # see FIXME below
import peewee
from playhouse.fields import PasswordField
from pytz import timezone

from chappy.config import Config
from chappy.models import User, Channel, ChannelUser, Message, init_db


app = Flask(__name__)
app.config.from_object(Config)

jwt = fj.JWTManager(app)
# socketio = SocketIO(app)

###################
# JWT SESSION SETUP
###################

# FIXME: get_jwt_identity is borked. Wrote my own:
def decode_identity():
    algorithm = fj.config.__dict__['ALGORITHM']
    secret = app.config.get('SECRET_KEY')
    token = request.headers.get('AUTHORIZATION').split(' ')[1]
    identity = jt.decode(token, secret, algorithm)
    return identity['identity']


@jwt.unauthorized_loader
def unauthorized_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 101,
        'log_message': 'User must login or provide valid JWT in request'
    }), 200


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 101,
        'log_message': 'JWT token has expired'
    }), 200



@app.route('/protected', methods=['GET'])

@fj.jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identitydecode_id()
    current_user = decode_identity()
    return jsonify({'hello_from': current_user}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'This would normally render a SPA homepage(?)'})


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return jsonify({"log_message": f"Successfully rendered the signup page"})
    else:
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
            return jsonify({"log_message": "Error! " u"😲  " "Check application logs"}), 400


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
def get_channel_participants(channel_id):
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
#FIXME: Should leaving a channel be nested? e.g /users/1/channels/1
@app.route('/channels/<int:channel_id>', methods=['POST', 'DELETE'])
def join_or_leave_channel(channel_id):
    user_id = decode_identity()
    username = User.get(User.id == user_id).username
    if request.method == 'POST':
        ChannelUser.get_or_create(user_id=user_id, channel_id=channel_id)
        return jsonify({"log_message": f"{username!r} successfully joined channel {channel_id!r}"})
    else: # DELETE
        delete_channel_users = ChannelUser.delete().where(
            ChannelUser.channel_id == channel_id and
            ChannelUser.user_id == user_id
        )
        delete_channel_users.execute()

        return jsonify({"log_message": f"{username!r} successfully left channel {channel_id!r}"})

@fj.jwt_required
@app.route('/channels/<int:channel_id>/messages', methods=['GET', 'POST'])
def fetch_or_send_to_channel(channel_id):
    user_id = decode_identity()
    if request.method == 'GET':
        messages = Message.select().where(Message.channel_id == channel_id)
        return jsonify([message.__dict__['_data'] for message in messages])
    else: #POST
        request_json = request.get_json()
        new_message = Message.create(
            channel_id=channel_id,
            user_id=user_id,
            text_content=request_json.get('textContent'),
            img_url=request_json.get('imgUrl'),
            video_url=request_json.get('videoUrl')
        )

        return jsonify(new_message.__dict__['_data'])

@fj.jwt_required
@app.route('/channels/<int:channel_id>/messages/<int:message_id>', methods=['PUT', 'DELETE'])
def edit_or_delete_message(channel_id,message_id):
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
        return jsonify(edited_message.__dict__['_data'])

    else: # DELETE
        Message.get(Message.id == message_id).delete_instance()
        return jsonify({"log_message": f"Successfully deleted message {message_id!r}"})

if __name__ == '__main__':
    from IPython import embed
    init_db()
    app.run(debug=Config.DEBUG)

