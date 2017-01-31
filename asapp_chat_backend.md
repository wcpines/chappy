# What I need to know how to do

### Application structure.

- Models
- Routes + controller actions/Flask; functions that return json
- mysql server(?)
- proxy server?


### Websockets

###Models

user has many messages through channels (sent)
user has many messages through channels ( received )
user has many channels



1. user.messages  => all message user has written
2. message.users => all users that received the message?

3.

- user has many messages
- user belongs to many messages (as recipient)

message has and belongs to many users?

- Create User model
  - name
  - email
  - password

- Conversation/Channel? (join two users and a message)
  - recipient ID
  - sender ID

- Messages
  - created_at
  - recipient
  - sender
  - text
  - img_link
  - video_link
  - img_size
  - video_length
  - video_source



### ORM

### Authentication

- JWT + password?

### Going to leave out

- Friends lists
- channels/threads/group messages
- correction of last message sent
- edit last message? (should be easy to get endpoint)
- delete last message? (should be easy to get endpoint)

#Goal


Basic chat backend

Support the following requests:

- **Create User**

Takes a user_name and password and creates a new user in a persisted data store.

- **Send Message**

Takes a sender, recipient, and message and saves that to the data store. Three different message types are supported. (1) is a basic text-only message. (2) is an image link. (3) is a video link. The image and video links are saved with some additional metadata (which can be hard-coded):

- width and height for the image,
- length of the video and source (YouTube, Vevo) for the video.

- **Fetch Messages**

Takes two users and loads all messages sent between them. This call should also take two optional parameters in order to support pagination: the number of message to show per page and which page to load.



Flow of the app:

1) Login and Auth
- @api.before_request except for login/signup
- verify_password => validate_auth_token
- User types in login user_name, and password
- Join channel




3) Send message
- (See message displayed above chat box, or, JSON returned with content)
- Message JSON: Text
- img_url:
