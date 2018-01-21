from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rbpi.settings')

app = Celery(
    'tasks',
    backend='amqp',
    broker='amqp://guest@localhost//')

# This reads, e.g., CELERY_ACCEPT_CONTENT = ['json'] from settings.py:
app.config_from_object('django.conf:settings')

# For autodiscover_tasks to work,
# you must define your tasks in a file called 'tasks.py'.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
