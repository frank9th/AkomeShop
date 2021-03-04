# Download the helper library from https://www.twilio.com/docs/python/install
import os
from decouple import config 
from django.conf import settings
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Hi there!',
                              from_='+19183471301',
                              to='+2349063630828'
                          )

print(message.sid)