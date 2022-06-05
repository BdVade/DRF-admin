# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../restadmin"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            "restadmin",
            "rest_framework",
            "tests"
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,

        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        SECRET_KEY='django-insecure-test-key',
        REST_FRAMEWORK={
            'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
            'TEST_REQUEST_RENDERER_CLASSES': [
                'rest_framework.renderers.MultiPartRenderer',
                'rest_framework.renderers.JSONRenderer',
                'rest_framework.renderers.TemplateHTMLRenderer', ],
            "DEFAULT_AUTHENTICATION_CLASSES": [
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.BasicAuthentication'
            ],
            "DEFAULT_PERMISSION_CLASSES": [
                'rest_framework.permissions.AllowAny',
            ]
        },

        TEMPLATES=[
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
        ],
    )
    django.setup()
