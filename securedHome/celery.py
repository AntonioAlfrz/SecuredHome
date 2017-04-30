from __future__ import absolute_import

import os
from datetime import timedelta
from celery import Celery
from django.conf import settings

from fcm_server import send_notification, token

project = "securedHome"

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project + '.settings')

app = Celery(project, broker='django://')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def task():
    for user in User.objects.all():
        new_token = Token.objects.get(user=User.objects.get(id=1)).generate_key()
        print "New token. Usuario: "+user+" Token: "+new_token
        Token.objects.filter(user=user).update(key=new_token)
        send_notification(token,None, {'token':new_token})
    return "Refreshing tokens"

app.conf.CELERYBEAT_SCHEDULE = {
    'token-refresh-every-1-minute': {
        'task': 'securedHome.celery.task',
        'schedule': timedelta(minutes=1),
        'relative': True,
    },
}

