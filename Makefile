URL=http://127.0.0.1:5000

.PHONY: run-test
run-test: post-signup \
	create-channel \
	get-channel-peeps \
	join-channel \
	leave-channel \
	send-message \
	fetch-messages\
	edit-message\
	delete-message


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
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels/1/messages textContent='a second message' imgUrl='https://images-na.ssl-images-amazon.com/images/G/01/img15/pet-products/small-tiles/23695_pets_vertical_store_dogs_small_tile_8._CB312176604_.jpg'
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels/1/messages textContent='a third message'

.PHONY: fetch-messages
fetch-messages:
	http --auth-type=jwt --auth=${TOKEN}: ${URL}/channels/1/messages

.PHONY: edit-message
edit-message:
	http --auth-type=jwt --json --auth=${TOKEN}: PUT ${URL}/channels/1/messages/1 textContent='an edited message!'

.PHONY: delete-message
delete-message:
	http --auth-type=jwt --auth=${TOKEN}: DELETE ${URL}/channels/1/messages/1


# curlput /channel/1/messages/1 '{"textContent": "test message for you!", "imgUrl": "", "videoUrl":""}'  # edit last message, diff on frontend?
# curldelete /channel/1/messages/1  # delete last message

