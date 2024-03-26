"""
Django settings for pdf_tool project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p9c1#di96)yp%3yjexpiyhn!)qnv*8=1d9nq+&pw@rd4w-%m#q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',  # for localhost (REACT Default)
    'http://localhost:8080',  # for localhost (Developlemt)
)

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  # for localhost (REACT Default)
    'http://localhost:8080',  # for localhost (Developlemt)
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pdf_tool.urls'

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

WSGI_APPLICATION = 'pdf_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Define the path to the log file
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'django.log')

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

import logging.config
import sys


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            # 'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            'format': '%(asctime)s|%(name)s|%(levelname)s|%(module)s:%(lineno)d|%(funcName)s|%(message)s'
        },
        'console': {
            'format': '%(asctime)s|%(name)s|%(levelname)s|%(module)s:%(lineno)d|%(funcName)s|%(message)s'

        }
    },
    'handlers': {
        'file': {
            'level': "DEBUG",
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOG_FILE,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],  # Include both file and console handlers
            'level': "DEBUG",
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)