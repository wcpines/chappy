# Chappy
*A sample chat app*

Supports the following requests:

**Create User**

Takes a username and password and creates a new user in a persisted data store.

**Send Message**

Takes a sender, recipient, and message and saves that to the data store. Three different message types are supported. (1) is a basic text-only message. (2) is an image link. (3) is a video link. The image and video links are saved with some additional metadata (which can be hard-coded):

- width and height for the image,
- length of the video and source (YouTube, Vevo) for the video.

**Fetch Messages**

Takes two users and loads all messages sent between them.

- This call should also take two optional parameters in order to support pagination:
- the number of message to show per page and which page to load.



## Models

*note* fields exclude id, created_at, updated_at

#### User

- has many messages (send)
- (has many messages through channels (receive))
- has many channels through channel users
- has many channelusers
  - username
  - email
  - phone (opt)
  - password

#### Message

- has one user (send)
- (has many users through channels (receive))
- has one channel
  - user_id
  - channel_id
  - text_content
  - img_url
  - video_url

#### Channel

- belongs to channeluser
- belongs to message
  - title


#### ChannelUser
- belongs to user
- belongs to channel
  - user_id
  - channel_id



## Authentication

- Password hashed
- JWT token issued for session persistence/resource auth

## Routes/actions

*by resource:*

#### User

- Create a new user (POST /signup)
- Login a user (POST /login)
- Edit user info (PUT /users/:id)
- Logout a user (remove the JWT from localstorage)

#### Channel

- Create a channel (POST /channels)
- Join channel (POST /channels/:id)  (create ChannelUser)
- Leave channel (DELETE /channels/:id) (delete ChannelUser)
- Delete channel ??  **FIXME**

#### Messages

- Fetch all messages for a given channel (GET /channel/:id/messages?)
- Send a message (POST /messages)

#### For later:

- Archive channel?  Note: how to route this vs *leaving* a channel

#### routes to be handled by react-router:

- get login page -- /login (GET)
- get signup page /signup (GET)
- get homepage (?)
- signout (state userId => null, remove jwt from cookie or localstorage)


```
curlget # misc health check
curlpost /signup JSON # signup, create user, get JWT
curlpost /login JSON # get JWT
curlget /channels  # get channel list
curlpost /channels JSON # create a channel/conversation
curlget /channels/1 # join a channel
curlpost /channels/1 JSON # join channel
curldelete /channels/1 JSON # leave channel
curlget /channel/1/messages # read all messages (limit most recent 50)
curlpost /channel/1/messages JSON # send a message to channel
curlput /channel/1/messages/1 JSON # edit last message
curldelete /channel/1/messages/1 JSON # delete last message
```
