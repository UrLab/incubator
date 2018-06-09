"""
Django settings for incubator project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.contrib.messages import constants as messages
import re


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cw2lz4ml1#r%=h2aax8_)=q$v(+&9&)n5xxk5g!9og%ityd!@#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'debug_toolbar',
    'bootstrap3',
    'datetimewidget',
    'rest_framework',
    'django_filters',
    'crispy_forms',
    'analytical',
    'constance',
    'constance.backends.database',

    'incubator',
    'events',
    'users',
    'projects',
    'space',
    'stock',
    'django_nyt',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'django_extensions',
    'realtime',
    'actstream',
    'manmail',
    'redir',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'incubator.urls'

WSGI_APPLICATION = 'incubator.wsgi.application'

SUIT_CONFIG = {
    'ADMIN_NAME': 'UrLab',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'SEARCH_URL': '/admin/users/user/',
    'MENU': (
        'users',
        {'app': "stock", 'models': ('product', 'category', 'producttransaction', 'topuptransaction', 'transfertransaction', 'misctransaction')},
        'constance',
        'actstream',
        'manmail',
        'redir',
    )
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-be'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "/"

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'incubator/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                "space.context_processors.state",
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'incubator.hashers.MediaWikiHasher',
)


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('incubator.drf.ReadOnlyPermission',),
    'DEFAULT_PAGINATION_CLASS': 'incubator.drf.AnachistPageNumberPagination',
    'UNICODE_JSON': False,
}

# no tailing slash
ROOT_URL = "https://urlab.be"


BANK_ACCOUNT = "BE66 0017 6764 5043"

REDIS_HOST = "rainbowdash.lan"
REDIS_PORT = 6379
FAKE_REDIS = True

USE_WAMP = False
CROSSBAR_URL = 'http://localhost:8080/publish'
CROSSBAR_SECRET = "Vairy secrette"
CROSSBAR_REALM = 'realm'

INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
INFLUX_USER = "derp"
INFLUX_PASS = "derp"

LOGIN_URL = '/auth/login/'

WIKI_ATTACHMENTS_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'tex',
    'py',
    'ppt',
    'pptx',
    'pdf',
    'zip',
    'tar',
    'gz',
)

ACTSTREAM_SETTINGS = {
    'USE_JSONFIELD': True
}

PIWIK_DOMAIN_PATH = 'piwik.urlab.be'
PIWIK_SITE_ID = '2'

MINIMAL_MAIL_APPROVERS = 3

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


CONSTANCE_ADDITIONAL_FIELDS = {
    'bootstrap-alert': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (("danger", "Rouge"), ("warning", "Orange"), ("info", "Bleu"), ("success", "Vert"))
    }],
}

CONSTANCE_CONFIG = {
    'PERIOD_OPEN': (True, 'Is the hackerspace supposed to be open during this period ?', bool),
    'HOMEPAGE_MESSAGE': ("", 'Message to show on the homepage (mardown accepted)', str),
    'HOMEPAGE_MESSAGE_TYPE': ("danger", "Color of the message to show on the homepage.", "bootstrap-alert"),

}

OPEN_WEEKDAYS = [0, 1, 2, 3, 4]  # Monday is day 0
OPEN_HOURS = list(range(7, 23))

EXPRESSIF_RANGES = [
    "18:fe:34", "24:0a:c4", "24:b2:de", "2c:3a:e8", "30:ae:a4", "3c:71:bf",
    "54:5a:a6", "5c:cf:7f", "60:01:94", "68:c6:3a", "84:0d:8e", "84:f3:eb",
    "90:97:d5", "a0:20:a6", "a4:7b:9d", "ac:d0:74", "b4:e6:2d", "bc:dd:c2",
    "c4:4f:33", "cc:50:e3", "d8:a0:1d", "dc:4f:22", "ec:fa:bc",
]

VMWARE_RANGES = [
    "00:05:69", "00:0c:29", "00:1c:14", "00:50:56",
]

OTHER_RANGES = [
    "00:16:3e",  # Xen
    "00:ca:fe",  # Xen
    "52:54:00",  # Qemu
    "00:15:5D",  # Hyper-V
]

MAC_RANGES = EXPRESSIF_RANGES + VMWARE_RANGES + OTHER_RANGES

IGNORE_LIST_RE = [
    re.compile(prefix + r'(:[0-9a-f]{2}){3}')
    for prefix in MAC_RANGES
]

try:
    from incubator.local_settings import * # NOQA
except ImportError:
    pass
