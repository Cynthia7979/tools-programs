# import smtplib
# from email.mime.multipart import MIMEMultipart
#
# server = smtplib.SMTP('smtp.sina.com', 25)
# server.login('goclare0412', 'd3f56529ea10a4f0')
# server.starttls()
# server.ehlo()
#
# message = "\ntest!"
# server.sendmail(from_addr='goclare0412@sina.com', to_addrs='goclare0412@sina.com', msg=message)

from twilio.rest import Client
client = Client([AUTH TOKEN REDACTED])
# client.messages.create(to="[PHONE NUMBER REDACTED]", from_="[PHONE NUMBER REDACTED]", body='Hello Twilio')

