from django.conf import settings

import os

import djcelery

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
            'djcelery',
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
            ('informer.models', 'DatabaseInformer'),
        ),
        BROKER_BACKEND = 'memory',
        CELERY_ALWAYS_EAGER = True,
        CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
    )

    djcelery.setup_loader()
