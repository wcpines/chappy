from twilio.rest import TwilioRestClient

from chappy.config import Config

client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])

def message_user(recipient_num, message):
    message = client.messages.create(
        body=message,
        to=recipient_num,
        from_num=app.config['SENDER_NUM']
    )

    print(message.sid)


