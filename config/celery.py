"""Celery Configuration.

This module contains configuration settings
for Celery, a distributed task queue.
Celery uses this configuration file to set up
the Celery application and define
settings such as the message broker,
result backend, task serialization format,
and other options.

For more information on Celery configuration options,
see the Celery documentation:
https://docs.celeryproject.org/en/stable/userguide/configuration.html
"""

import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Method for making periodic tasks
    :param sender:
    :param kwargs:
    :return:
    """
    sender.add_periodic_task(
        crontab(minute="0", hour="0"),
        clear_blacklisted_tokens.s(),
        name="clear expired tokens everyday",
    )


app.conf.timezone = "Europe/Kiev"


@app.task
def clear_blacklisted_tokens():
    """Task for clearing blacklisted tokens in system
    :return:
    """
    from ninja_jwt.token_blacklist.models import OutstandingToken
    from ninja_jwt.utils import aware_utcnow

    (OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete())
