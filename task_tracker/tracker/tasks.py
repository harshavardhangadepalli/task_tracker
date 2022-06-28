import smtplib
from smtplib import SMTPException
from typing import List

from celery import task

# this file is the file that is used to create a celery task for sending email.
@task(name="send email")
def send_mail(sender: str, receivers: List[str], message: str):
    try:
        smtpObj = smtplib.SMTP("localhost", port=3000)
        smtpObj.sendmail(sender, receivers, message)
        print("Mail sent successfully")
    except SMTPException:
        print("failed to send mail")
