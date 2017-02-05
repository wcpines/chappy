import peewee
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask import Flask, g, redirect, request, session, url_for, abort, jsonify
from flask_socketio import SocketIO, send, emit
from IPython import embed
from pytz import timezone


#  EST = timezone('US/Eastern')
#  UTC = timezone('UTC')

app = Flask(__name__)

# toggle between development/production using env var
app.config.from_object(os.environ['APP_SETTINGS']) # config.DevConfig
db = peewee.SqliteDatabase(app.config['DATABASE'], threadlocals=True)

jwt = JWTManager(app)
socketio = SocketIO(app)

# import after db/config setup
from models import *


def init_db():
    db.connect()

    #  NOTE: Testing purposes only!
    ################################################################
    ################################################################
    tables = [User, Channel, Message, ChannelUser]
    for table in tables:
        try:
            drop_table(table)
        except Exception as e:
            print("Failed to drop {}; {}".format(table, e.args[0]))
    ################################################################
    ################################################################

    db.create_tables([User, Channel, Message, ChannelUser], safe=True)


###################
# JWT SESSION SETUP
###################

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

            jwt = {'access_token': create_access_token(identity=user.id)}
            return jsonify(jwt), 200

        except Exception as e:
            #  return jsonify({"log_message": "{} already in use".format(e.args[0].split(".")[-1])})
            return jsonify({"log_message": "ERROR TYPE: {}, ERROR: {}".format(type(e), e.args[0])}), 400


@app.route('/login', methods=['POST'])
def login():
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    user = User.get(User.email == 'email')

    if user and user.check_password(passward): # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#PasswordField
        jwt = {'access_token': create_access_token(identity=user.id)}
        return jsonify(jwt), 200
    else:
        return jsonify({"log_message": "Bad username or password"}), 401


# creating a conversation *requires* two users, inviter and invitee
# @jwt_required
@app.route('/channels', methods=['POST'])
def create_channel():
    user_id = get_jwt_identity()
    title = request.get_json().get('title')
    channel_invitee_id = request.get_json().get('channelInviteeId')
    channel = Channel.create(title=title)
    ChannelUser.get_or_create(user_id=channel_invitee_id, channel_id=channel.id)
    ChannelUser.get_or_create(user_id=user_id, channel_id=channel.id)
    return jsonify({"log_message": f"Successfully left channel {channel_id!r}"})

# @jwt_required
@app.route('/channels/<int:channel_id>', methods=['GET'])
def get_channel_participants(channel_id):
    channel_users = ChannelUser.select(ChannelUser.channel_id == channel_id)
    #  e.g. ChannelUser(id=1, user_id=1, channel_id=1)
    user_ids = [user_id.user_id for user_id in channel_users]
    users = User.select(User.id << user_ids)
    return jsonify(users) # <= return an array of user objects

# @jwt_required
@app.route('/channels/<int:channel_id>', methods=['POST', 'DELETE'])
def join_or_leave_channel(channel_id):
    # user_id = get_jwt_identity()
    if request.method == 'POST':
        ChannelUser.get_or_create(user_id=user_id, channel_id=channel_id)
        return jsonify({"log_message": f"Successfully joined channel{channel_id!r}"})
    else: # DELETE
        channel_users = ChannelUser.select().where(
            ChannelUser.channel_id == channel_id and
            ChannelUser.user_id == user_id
        ).delete_instance()
        return jsonify({"log_message": f"Successfully left channel {channel_id!r}"})

# @jwt_required
@app.route('/channel/<int:channel_id>/messages', methods=['GET', 'POST'])
def fetch_or_send_to_channel(channel_id):
    # user_id = get_jwt_identity()
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
        )
        return jsonify(new_message)

# @jwt_required
@app.route('/channel/<int:channel_id>/messages/<int:message_id>', methods=['PUT', 'DELETE'])
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
    embed()
    init_db()
    app.run()
    #  socketio.run(app)



#  TODO (goals):
    #  AUTH
        #  When a user signs up, hash and save password
        #  When a user logs in, check their password (hashed) against the saved password (hashed)
        #  If they match, respond with a JSON Web token to persist their session, with a default expiry of 30 days
        #  When a user requests a route other than login, check their request for a JSON token and use their user ID.
        #  If the User ID doesn't exist, route to login page

    #  - Assign written message to a user, and message can be sent to a receiver
    #   (based on ID specified? Based on join object/relation?)
    #  - create users, authenticate users
    #  - write and retrieve over a socket connection



