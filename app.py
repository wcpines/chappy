from flask import Flask, g, redirect, request, session, url_for, abort, jsonify
#  from helpers import issue_token, before_request, after, login_required
from flask_socketio import SocketIO, send, emit
from peewee import SqliteDatabase
from IPython import embed
import os

from pytz import timezone

est = timezone('US/Eastern')
UTC = timezone('UTC')

app = Flask(__name__)

# toggle between development/production using env var
app.config.from_object(os.environ['APP_SETTINGS']) # config.DevConfig
db = SqliteDatabase(app.config['DATABASE'], threadlocals=True)

socketio = SocketIO(app)

# import after db/config setup
from models import *

def init_db():
    db.connect()
    db.create_tables([Message], safe=True)
    #  db.create_tables([User, Channel, Message], safe=True)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'This would normally render a SPA homepage(?)'})

# TODO: What are the restful route conventions for a given resource in flask?
@app.route('/message', methods=['GET','POST'])
def fetch_or_create():
    if request.method == 'GET':
        messages = Message.select()
        embed()
        #  return jsonify({'messages': [UTC.localize]})
        return jsonify({'message' : 'Hello from the /message route [GET]'})
    else:
        request_json = request.get_json()
        new_message = Message.create(
            text_content=request_json['message'],
            img_url=request_json.get('imgUrl'),
            video_url=request_json.get('videoUrl')
        )
        return jsonify(request.get_json()['message'])


@app.route('/message/<int:id>', methods=['GET, PUT'])
def show_or_edit():
    return jsonify({'message' : 'This would normally render a SPA homepage'})

# allow running from the command line
if __name__ == '__main__':
    init_db()
    app.run()
    #  socketio.run(app)



# FIXME (questions):
    #  - Database connections are failing.
    #  - best way to do restful routes for a given resoure (can I avoid flask-RESTful?)
    #  - best way to actually organize the app. Init file? Import sanity?


    #  - how are users and messages connected.  Many-to-many through channels?
    #  - authenticating users


#  TODO (goals):
    #  - write and retrieve basic message objects in the DB
    #  - Assign written message to a user, and message can be sent to a receiver (based on ID specified? Based on join object/relation?)
    #  - create users, authenticate users
    #  - write and retrieve over a socket connection
