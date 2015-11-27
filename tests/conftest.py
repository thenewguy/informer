# coding: utf-8

from __future__ import absolute_import

from django.conf import settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pytest_configure():
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'informer'),
        MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.security.SecurityMiddleware',
        ),
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                #  'ENGINE': 'django.db.backends.postgresql_psycopg2',
                #  'NAME': 'postgres',
                'USER': 'postgres',
                'HOST': 'postgres',
                'PORT': '5432',
            }
        },
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        },
        TEMPLATES = [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        }],
        ROOT_URLCONF = 'informer.urls',
        STATIC_URL = '/static/',
        STATIC_ROOT = '/static/',
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, 'static'),
        ),
        DJANGO_INFORMERS = (
            ('informer.checker.database', 'DatabaseInformer'),
            ('informer.checker.storage', 'StorageInformer'),
            ('informer.checker.celery', 'CeleryInformer'),
            ('informer.checker.cache', 'CacheInformer'),
        ),
        DJANGO_INFORMER_PREVENT_SAVE_UNTIL = 5,
        BROKER_BACKEND = 'memory',
        BROKER_URL='memory://',
        CELERY_ALWAYS_EAGER = True,
        CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
        CELERY_ACCEPT_CONTENT = ['json'],
    )
