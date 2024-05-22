# -*- coding: utf-8 -*-
"""
Celery Configuration.

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
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "config.settings.settings")

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.timezone = "Europe/Kiev"
