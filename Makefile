URL=http://127.0.0.1:5000

.PHONY: run-test
run-test: home \
	get-signup \
	post-signup \
	create-channel \
	get-channel-peeps \
	join-channel \
	leave-channel \
	send-message


.PHONY: home
home:
	http ${URL}

.PHONY: get-signup
get-signup:
	http ${URL}/signup

.PHONY: post-signup
post-signup:
	http --json POST ${URL}/signup username='wcpines' email='wcpines@gmail.com' password='testing'
	http --json POST ${URL}/signup username='testUser' email='bla@bla.com' password="testing1"


TOKEN=$(shell echo `http --json POST ${URL}/login email='wcpines@gmail.com' password='testing' | jq --raw-output .access_token`)

.PHONY: create-channel
create-channel:
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels title='test channel' channelInviteeId:=2

.PHONY: get-channel-peeps
get-channel-peeps:
	http --auth-type=jwt --auth=${TOKEN}: ${URL}/channels/1

.PHONY: join-channel
join-channel:
	http --auth-type=jwt --auth=${TOKEN}: POST ${URL}/channels/1

.PHONY: leave-channel
leave-channel:
	http --auth-type=jwt --auth=${TOKEN}: DELETE ${URL}/channels/1

.PHONY: send-message
send-message:
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels/1/messages textContent='a new message' videoUrl='https://www.youtube.com/watch?v=nHSESdnfpOk'


# curlpost /channels/1 # join a channel
# curldelete /channels/1 # leave channel
# curlget /channel/1/messages # read all messages (limit most recent 50)
# curlpost /channel/1/messages '{"textContent": "test message for you!", "imgUrl": "", "videoUrl":""}' # send a message to channel
# curlput /channel/1/messages/1 '{"textContent": "test message for you!", "imgUrl": "", "videoUrl":""}'  # edit last message, diff on frontend?
# curldelete /channel/1/messages/1  # delete last message

