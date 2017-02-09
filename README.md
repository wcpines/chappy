<!-- vim-markdown-toc Redcarpet -->
* [Chappy](#chappy)
    * [Sample services](#sample-services)
      * [Create User](#create-user)
      * [Create a Channel](#create-a-channel)
      * [Send a Message](#send-a-message)
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
*A sample chat app*


### Sample services

*Complete list of services below under* [Routes/actions](#routes-actions)

####Create User

POST `/signup`
Takes a username and password and creates a new user.

####Create a Channel

POST `/channels`

Takes the current user's id, an invitee id (second user ID), and a title.

***NB:***
  - Deleting/archiving a channel is not yet supported
  - Currently no record of channel creator/inviter

####Send a Message

POST `/channels/[channel_id]/messages`
Takes a sender, recipient, and various message fields (see below), save it to the data store.  Three different message types are supported:

1. text-only
2. image (url)
3. video (url)

If a video link is present, the img URL is ignored.
If either media type is present, the API will call a third party API (embedly) to populate the following metadata:

- width and height for the image, an embeddable img URL
- length of the video, source domain, an embeddable iframe


**Fetch Messages**

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

Passwords are hashed server-side via Peewee builtin: PasswordField, which uses bcrypt

JWT tokens are for session persistence/resource authorization

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

- Fetch all messages for a given channel (GET  `/channels/<int:channel_id>/messages`
- Send a message (POST `/channels/<int:channel_id>/messages`)
