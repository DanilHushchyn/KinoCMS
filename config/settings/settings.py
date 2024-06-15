"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# django-environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [env('DJANGO_ALLOWED_HOSTS')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    "django.contrib.postgres",
    'django.contrib.sites',
    "modeltranslation",
    # "debug_toolbar",
    'ninja_jwt.token_blacklist',
    "requests_tracker",
    "corsheaders",
    "imagekit",
    "django_extensions",
    "ninja_jwt",
    "django_cleanup.apps.CleanupConfig",
    "ninja_extra",
    "meta",
    'multiselectfield',
    "phonenumber_field",
    'django_countries',
    'src.authz',
    'src.booking',
    'src.cinemas',
    'src.core',
    'src.movies',
    'src.pages',
    'src.users',
    'src.mailing',
]
AUTH_USER_MODEL = "users.User"

PASSWORD_RESET_TIMEOUT = 1800  # 30 minutes
#
AUTHENTICATION_BACKENDS = [
    "src.users.authentication.EmailBackend",
]
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Change the token expiration time to 30 minutes
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),  # Here we have Redis DSN (for ex. redis://localhost:6379/1)
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_ENTRIES": 1000  # Increase max cache entries to 1k (from 300)
        },
    }
}
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'django_redis.client.DefaultClient'

SITE_ID = 1
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=25),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=5),
    # For Controller Schemas
    # FOR OBTAIN PAIR
    "TOKEN_OBTAIN_PAIR_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainPairInputSchema",
    "TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshInputSchema",
    # FOR SLIDING TOKEN
    "TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainSlidingInputSchema",
    "TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshSlidingInputSchema",
    "TOKEN_BLACKLIST_INPUT_SCHEMA": "ninja_jwt.schema.TokenBlacklistInputSchema",
    "TOKEN_VERIFY_INPUT_SCHEMA": "ninja_jwt.schema.TokenVerifyInputSchema",
}
NINJA_EXTRA = {
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:1337",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://gold-boost.netlify.app",
    "http://127.0.0.1",
    "https://goodboost-spacelab.avada-media-dev2.od.ua",
    "https://kinocms-panel.demodev.cc",
]
# ROOT_URLCONF = 'config.urls'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
# ABSOLUTE_URL = f'{env("MEDIA_URL")}'

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ABSOLUTE_URL = env('ABSOLUTE_URL')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
USE_I18N = True

LANGUAGE_CODE = "uk"

TIME_ZONE = "Europe/Kiev"

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

LANGUAGES = [
    ("uk", "Ukrainian"),
    ("ru", "Russian"),
]

MODELTRANSLATION_LANGUAGES = ("uk", "ru")
# MODELTRANSLATION_FALLBACK_LANGUAGES = {'default': ('en',)}
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR)/"media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
