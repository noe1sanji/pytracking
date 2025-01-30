import os
from email.message import EmailMessage
from smtplib import SMTP_SSL

from dotenv import load_dotenv

load_dotenv()

config = {}

try:
    config["user"] = os.environ["GMAIL_USERNAME"]
    config["password"] = os.environ["GMAIL_PASSWORD"]
except KeyError:
    print("GMAIL_USERNAME or GMAIL_PASSWORD not found in .env")


def send_mail(subject: str, to: str | tuple, message: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config["user"]
    msg["To"] = to
    msg.set_content(message)
    msg.add_alternative(message, subtype="html")

    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(config["user"], config["password"])
        smtp.send_message(msg)
