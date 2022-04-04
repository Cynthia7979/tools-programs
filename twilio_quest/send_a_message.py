import os
from twilio.rest import Client

account_sid, auth_token = input('Enter Account SID: '), input('Enter Authentication Token: ')
client = Client(account_sid, auth_token)

msg = client.messages.create(
    from_="+12542745237",
    body='Hello TwilioQuest!',
    to=input('Enter authenticated phone number: ')
)

print(msg.sid)
