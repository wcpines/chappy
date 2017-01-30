from flask import Flask, g, redirect, request, session, url_for, abort, jsonify
from flask_socketio import SocketIO, send
from functools import wraps
from models import *
from auth import *

# config - aside from our database, the rest is for use by Flask

app.config.from_object('config.BaseConfig')
app = Flask(__name__)
socketio = SocketIO(app)

#  # simple utility function to create tables
def init_db():
    database.connect()
    database.create_tables([User, Relationship, Message], safe=True)


@app.route ('/api/login', methods=['GET'])
def index():
    return render_template('frontend_mockup.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@socketio.on('send_message')
def handle_my_custom_event(json):
    print(json)

@socketio.on('receive_message')



# allow running from the command line
if __name__ == '__main__':
    init_db()
    socketio.run(app)


#  routes:

#      /login (post)
#      /logout (post)
#      /channels/<:channel_id> (get?)
#      /message/send (post)


# Flow of the app:

# 1. User login
# 2. Join channel
# 3. Send message
# 4. (See message displayed above chat box, or, JSON returned with content)
# 5. Message JSON: Text
# 6. img_url:
