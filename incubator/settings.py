"""
Django settings for incubator project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import re
import sentry_sdk

from django.contrib.messages import constants as messages
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "vairysecrette")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", "1")))


ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,::1,localhost").split(
    ","
)
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

if SENTRY_DSN != "":
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "bootstrap4",
    "rest_framework",
    "django_filters",
    "crispy_forms",
    "constance",
    "constance.backends.database",
    "simple_history",
    "incubator",
    "events",
    "users",
    "projects",
    "badges",
    "space",
    "stock",
    "streams",
    "django_nyt",
    "mptt",
    "wiki",
    "sekizai",
    "sorl.thumbnail",
    "django_extensions",
    "realtime",
    "actstream",
    "manmail",
    "redir",
)

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "incubator.middleware.AdminAccessMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
)

ROOT_URLCONF = "incubator.urls"

WSGI_APPLICATION = "incubator.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "fr-be"

TIME_ZONE = "Europe/Brussels"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "/"

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "incubator/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "space.context_processors.state",
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]


PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.CryptPasswordHasher",
    "incubator.hashers.MediaWikiHasher",
)


MESSAGE_TAGS = {messages.ERROR: "danger"}

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("incubator.drf.ReadOnlyPermission",),
    "DEFAULT_PAGINATION_CLASS": "incubator.drf.AnachistPageNumberPagination",
    "UNICODE_JSON": False,
}

# no tailing slash
ROOT_URL = "https://urlab.be"


BANK_ACCOUNT = "NOT AVAILABLE FOR NOW"

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = 6379
FAKE_REDIS = int(os.environ.get("FAKE_REDIS", 0))

USE_WAMP = False
CROSSBAR_URL = "http://localhost:8080/publish"
CROSSBAR_SECRET = "Vairy secrette"
CROSSBAR_REALM = "realm"

USE_MQTT = False
MQTT_HOST = "localhost"

INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
INFLUX_USER = "derp"
INFLUX_PASS = "derp"

LOGIN_URL = "/auth/login/"

WIKI_ATTACHMENTS_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "tex",
    "py",
    "ppt",
    "pptx",
    "pdf",
    "zip",
    "tar",
    "gz",
)

ACTSTREAM_SETTINGS = {"USE_JSONFIELD": True}

MINIMAL_MAIL_APPROVERS = 3

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"


CONSTANCE_ADDITIONAL_FIELDS = {
    "bootstrap-alert": [
        "django.forms.fields.ChoiceField",
        {
            "widget": "django.forms.Select",
            "choices": (
                ("danger", "Rouge"),
                ("warning", "Orange"),
                ("info", "Bleu"),
                ("success", "Vert"),
            ),
        },
    ],
}

CONSTANCE_CONFIG = {
    "PERIOD_OPEN": (
        True,
        "Is the hackerspace supposed to be open during this period ?",
        bool,
    ),
    "HOMEPAGE_MESSAGE": ("", "Message to show on the homepage (mardown accepted)", str),
    "HOMEPAGE_MESSAGE_TYPE": (
        "danger",
        "Color of the message to show on the homepage.",
        "bootstrap-alert",
    ),
    "LIVESTREAM_URL": ("", "Url of the .flv endpoint for the livestream", str),
}

OPEN_WEEKDAYS = [0, 1, 2, 3, 4]  # Monday is day 0
OPEN_HOURS = list(range(7, 23))

EVENTS_PER_PAGE = 40

EXPRESSIF_RANGES = [
    "18:fe:34",
    "24:0a:c4",
    "24:b2:de",
    "2c:3a:e8",
    "30:ae:a4",
    "3c:71:bf",
    "54:5a:a6",
    "5c:cf:7f",
    "60:01:94",
    "68:c6:3a",
    "84:0d:8e",
    "84:f3:eb",
    "90:97:d5",
    "a0:20:a6",
    "a4:7b:9d",
    "ac:d0:74",
    "b4:e6:2d",
    "bc:dd:c2",
    "c4:4f:33",
    "cc:50:e3",
    "d8:a0:1d",
    "dc:4f:22",
    "ec:fa:bc",
]

VMWARE_RANGES = [
    "00:05:69",
    "00:0c:29",
    "00:1c:14",
    "00:50:56",
]

OTHER_RANGES = [
    "00:16:3e",  # Xen
    "00:ca:fe",  # Xen
    "52:54:00",  # Qemu
    "00:15:5D",  # Hyper-V
    "b8:27:eb",  # Raspberry-Pi
]

MAC_RANGES = EXPRESSIF_RANGES + VMWARE_RANGES + OTHER_RANGES

IGNORE_LIST_RE = [re.compile(prefix + r"(:[0-9a-f]{2}){3}") for prefix in MAC_RANGES]

EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 25))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", default="contact@urlab.be")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_FROM", default="contact@urlab.be")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", default=True)
