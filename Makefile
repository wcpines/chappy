URL=http://127.0.0.1:5000

.PHONY: run-test
run-test: post-signup \
	create-channel \
	join-channel \
	leave-channel \
	send-message \
	send-img-message \
	send-video-message \
	fetch-messages-with-offset \
	edit-message \
	delete-message


.PHONY: post-signup
post-signup:
	http --json POST ${URL}/signup username='wcpines' email='wcpines@gmail.com' password='testing'
	http --json POST ${URL}/signup username='testUser' email='bla@bla.com' password="testing1"

# login:
TOKEN=`http --json POST ${URL}/login email='wcpines@gmail.com' password='testing' | jq --raw-output .access_token`

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
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels/1/messages textContent='this message has no media'

.PHONY: send-img-message
send-img-message:
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels/1/messages textContent='this message has an image link' imgUrl='https://images-na.ssl-images-amazon.com/images/G/01/img15/pet-products/small-tiles/23695_pets_vertical_store_dogs_small_tile_8._CB312176604_.jpg'

.PHONY: send-video-message
send-video-message:
	http --auth-type=jwt --json --auth=${TOKEN}: POST ${URL}/channels/1/messages textContent='this message has a video link' videoUrl='https://www.youtube.com/watch?v=nHSESdnfpOk'

.PHONY: fetch-messages-with-offset
fetch-messages-with-offset:
	http --auth-type=jwt --auth=${TOKEN}: ${URL}/channels/1/messages?offset=1\&limit=50

.PHONY: edit-message
edit-message:
	http --auth-type=jwt --json --auth=${TOKEN}: PUT ${URL}/channels/1/messages/1 textContent='an edited message!'

.PHONY: delete-message
delete-message:
	http --auth-type=jwt --auth=${TOKEN}: DELETE ${URL}/channels/1/messages/1
