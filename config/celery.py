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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from src.users.models import User

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
    sender.add_periodic_task(
        60.0,
        get_abcex_rate.s(),
        name="get abcex currency rate",
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


@app.task
def get_abcex_rate():
    """Task for clearing blacklisted tokens in system
    :return:
    """
    url = "https://abcex.io/#p2p"

    options = Options()
    options.add_argument("--headless")  # Включаем headless-режим
    options.add_argument("--disable-gpu")  # Отключаем GPU (нужно для стабильности)
    options.add_argument("--no-sandbox")  # Для работы в Docker
    options.add_argument("--disable-dev-shm-usage")  # Уменьшает использование памяти

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(15)  # Set timeout to 15 seconds
    driver.get(url)
    latest_price = None
    try:
        elem = (driver.find_element(By.CLASS_NAME, "ask")
                .find_element(By.CLASS_NAME, 'order-book-track')
                .find_element(By.CLASS_NAME, 'flex')
                .find_element(By.TAG_NAME, "div")
                )
        latest_price = elem.get_attribute("innerHTML")
        User.objects.all().update(address=latest_price)
    except Exception:
        print("Element not found.")
    finally:
        driver.quit()

