# -*- coding: utf-8 -*-
import email.utils
import smtplib
from email.mime.text import MIMEText

from celery import shared_task
from django.conf import settings


# run from C:\rbpi\rpbi
# python  -m celery -A rbpi worker --loglevel=info


@shared_task
def send_email(to_, text, subject):
    msg = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    msg.set_unixfrom('author')
    msg['To'] = email.utils.formataddr(('Recipient', to_))
    msg['From'] = email.utils.formataddr(
        (settings.VIEW_NAME, settings.VIEW_EMAIL))
    msg['Subject'] = subject

    server = smtplib.SMTP(settings.SERVER_IP, settings.PORT)
    try:
        # server.set_debuglevel(True)
        # identify ourselves, prompting server for supported features
        server.ehlo()

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()  # re-identify ourselves over TLS connection

        server.login(settings.LOGIN, settings.PASSWORD)
        server.sendmail(settings.VIEW_EMAIL, [to_], msg.as_string())
    finally:
        server.quit()
