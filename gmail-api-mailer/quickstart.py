from Google import create_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

print(service.users().getProfile(userId='me').execute())

emailMsg = 'This is it'
mimeMessage = MIMEMultipart()

mimeMessage['to'] = 'emailmeonmyfakeemailid@gmail.com'
mimeMessage['from'] = 'Austin Myles<austinmyles289@gmail.com>'
mimeMessage['subject'] = 'You know'+str(random.randint(1000, 9999))
mimeMessage.attach(MIMEText(emailMsg, 'plain'))

raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)