from string import Template as tplt
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
        return tplt(template_file_content)

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


names, emails = get_contacts('mycontacts.txt')
print(names, emails)

img_data = open('index.png', 'rb').read()
# Create SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587) 

# Start TLS for security
s.starttls()

#Authentication
userEmail = input("Enter your email: ")
password = input("Enter your password: ")

status = s.login(userEmail, password)
print(status)

message_template = read_template('message.txt')
for name, email in zip(names, emails):
    msg = MIMEMultipart()       # create a message
    message = message_template.substitute(PERSON_NAME=name.title())
    msg['From']=userEmail
    msg['To']=email
    msg['Subject']="This is TEST"
    msg.attach(MIMEText(message, 'plain'))
    image = MIMEImage(img_data, name=os.path.basename('index.png'))
    msg.attach(image)
    s.send_message(msg)
    del msg
s.quit()
