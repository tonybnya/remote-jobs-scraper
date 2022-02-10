import ssl
import smtplib
from datetime import datetime
from pushbullet import Pushbullet
from plyer import notification


def pushify(API_KEY, jobs):
    """
    Function to send push notifications to my phone using Pushbullet App
    and `pushbullet` module.
    """

    pb = Pushbullet(API_KEY)
    now = datetime.now()
    current_date = now.strftime("%m-%d-%Y")
    push = pb.push_note(f"Date: {current_date}\n", jobs)


def gmail_sender(message):
    """
    Function to send email via Gmail.
    """

    port = 465
    smtp_server = "smtp.gmail.com"
    sender = "nya.tony2010@gmail.com"
    receiver = "nya.tony2010@gmail.com"
    password = "my-gmail-password for apps"  # myaccount.google.com/security

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender, password)
            response = server.sendmail(sender, receiver, message)
            print("Email sent!")
        except:
            print("Could not login or send the mail.")
