from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC792553ef34c97e77a7ab3faa9d8e4d66'
auth_token = 'e65120412da3b27113b174227f4f9f13'
sender="+15642030088"
client = Client(account_sid, auth_token)


def sendSMS(recipient,body):
    message = client.messages \
                    .create(
                        body=body,
                        from_=sender,
                        to="+91"+recipient
                    )

    print(message.sid)