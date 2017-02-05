
.PHONY: test-thing
test-thing:
	echo 'test from the Makefile'


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

