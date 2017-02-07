from twilio.rest import TwilioRestClient

from chappy.config import Config

client = TwilioRestClient(Config.TWILIO_SID, Config.TWILIO_API_KEY)

def message_user(recipient_num, message):
    message = client.messages.create(
        body=message,
        to=recipient_num,
        from_num=Config.TWILIO_NUMBER
    )

    print(message.sid)


