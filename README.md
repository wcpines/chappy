<!-- vim-markdown-toc Redcarpet -->
* [Chappy](#chappy)
  * [Installation](#installation)
    * [Sample services](#sample-services)
      * [Create User](#create-user)
      * [Create a Channel](#create-a-channel)
      * [Send a Message](#send-a-message)
      * [Fetch Channel Messages](#fetch-channel-messages)
  * [Models](#models)
      * [User](#user)
      * [Message](#message)
      * [Channel](#channel)
      * [ChannelUser](#channeluser)
  * [Authentication](#authentication)
  * [Routes/actions](#routes-actions)
      * [User](#user)
      * [Channel](#channel)
      * [Messages](#messages)

<!-- vim-markdown-toc -->
# Chappy
*A sample chat app backend -- WIP*


The current version does not have websockets completely implemented. A front-end client would need to poll for new messages every few seconds.

## Installation

1. Clone the repository

  ```sh
  git clone git@github.com:wcpines/chappy.git
  ```

2. Create a virtual environment and source it

  ```sh
  virtualenv chappy
  source chappy/bin/activate
  ```

3. Install dependencies:

  ```sh
   pip install -r requirements.txt
  ```

**NB: The following environment variables must be defined in order to run the app:**


```sh
export SECRET_KEY=[YOUR OWN SECRET]
export FLASK_SECRET_KEY_BASE=[YOUR OWN KEY BASE]
export EMBEDLY_API_KEY=[YOUR OWN API KEY]
```


To test, run the server, and in a separate shell session, run make:

```sh
$ PYTHONPATH=. python chappy/app.py
```


```sh
$ make
```


### Sample services

*Complete list of services below under* [Routes/actions](#routes-actions)

#### Create User

POST `/signup`
Takes a username and password and creates a new user.

#### Create a Channel

POST `/channels`

Takes the current user's id, an invitee id (second user ID), and a title.

*Note:*

- Deleting/archiving a channel is not yet supported
- Currently there is no record of a channel's creator/admin

#### Send a Message

POST `/channels/[channel_id]/messages`
Takes a sender, recipient, channel_id, and various message fields (see below).  Three different message types are supported:

1. text-only
2. image (url)
3. video (url)

If a video url is present, the image URL is ignored.
If either media type is present, chappy performs a third-party API call to Embedly, and populates the following metadata:

- width and height for the image
- length of the video, source domain, an embeddable iframe with the video


#### Fetch Channel Messages

Loads all messages for a given channel. Takes two optional parameters in order to support pagination:

- `limit`: the number of messages to show per page
- `offset`: which page to load


## Models

*NB* listed fields exclude `id`, `created_at`, `updated_at`

#### User

- has many messages (send)
- [has many messages through channels (receiving)]
- has many channels through channelusers
- has many channelusers
  - `username`
  - `email`
  - `phone` (opt)
  - `password`

#### Message

- has one user (send)
- [has many users through channels (receive)]
- has one channel
  - `user_id`
  - `channel_id`
  - `text_content`
  - `img_url`
  - `img_html`
  - `img_height`
  - `img_width`
  - `video_url`
  - `video_html`
  - `video_source`
  - `video_length`

#### Channel

- belongs to channeluser
- belongs to message
  - `title`


#### ChannelUser
- belongs to user
- belongs to channel
  - `user_id`
  - `channel_id`

## Authentication

Passwords are hashed server-side via the Peewee ORM's builtin `PasswordField`, which uses bcrypt.

JWT tokens are for session persistence/resource authorization.

## Routes/actions

#### User

- Create a new user (POST `/signup`)
- Login a user (POST `/login`)
- Edit user info (PUT `/users/<int:user_id>`)

#### Channel

- Create a channel (POST `/channels`)
- Join channel (POST `/channels/<int:channel_id>`)  (create ChannelUser)
- Leave channel (DELETE `/channels/:id`) (deletes ChannelUser)

#### Messages

- Fetch all messages for a given channel (GET  `/channels/<int:channel_id>/messages`)
- Send a message (POST `/channels/<int:channel_id>/messages`)
- Edit a message (PUT `/channels/<int:channel_id>/messages/<int:message_id>`)
- Delete a message (Delete `/channels/<int:channel_id>/messages/<int:message_id>`)
