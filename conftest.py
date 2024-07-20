"""Configuration file for pytest,
contains fixtures, connection to test scenaries
and init blocks
"""

import os
from pathlib import Path

import environ
import psycopg2
import pytest
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# django-environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


def run_sql(sql):
    conn = psycopg2.connect(database="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings

    the_source_db = settings.DATABASES["default"]["NAME_TEST"]
    # run_sql('DROP DATABASE IF EXISTS the_copied_db')
    run_sql(f"CREATE DATABASE test_{the_source_db} TEMPLATE {the_source_db}")

    yield

    for connection in connections.all():
        connection.close()

    run_sql(f"DROP DATABASE test_{the_source_db}")
