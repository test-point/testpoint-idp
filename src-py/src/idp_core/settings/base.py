# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = env('IDP_SECRET_KEY', default='some long random value, kept in secret, used for some signatures')

DEBUG = env.bool('IDP_DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # we use Sentry to be informed about any errors, use IDP_RAVEN_DSN env variable to configure it
    'raven',

    'idp_core',
    'idp_core.users',
    'idp_core.rp',
    'oidc_provider',  # 3rd party Django app

    # 'storages',  # deployment requirement, may be removed for local and gunicorn-based installations, but useful for zappa and heroku-like
    'crispy_forms',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'idp_core.urls'

WSGI_APPLICATION = 'idp_core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('IDP_DB_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': env('IDP_DB_NAME', default='simguard'),
        'HOST': env('IDP_DB_HOST', default='localhost'),
        'PORT': env('IDP_DB_PORT', default=5432),
        'USER': env('IDP_DB_USERNAME', default='simguard'),
        'PASSWORD': env('IDP_DB_PASSWORD', default='simguard'),
        'ATOMIC_REQUESTS': True,
    }
}

LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = env('IDP_STATIC_URL', default='/static/')
STATIC_ROOT = os.path.join(BASE_DIR, '../../var/staticroot/')
STATICFILES_STORAGE = env(
    "IDP_STATICFILES_STORAGE",
    default="django.contrib.staticfiles.storage.StaticFilesStorage"
)

# Custom settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'owner', 'administrator', 'root']
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_ADAPTER = 'idp_core.users.adapters.OurAllauthAdapter'
SOCIALACCOUNT_ADAPTER = 'idp_core.users.adapters.OurAllauthSocialAdapter'
ACCOUNT_USER_DISPLAY = 'idp_core.users.adapters.user_email_display'
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# OIDC Provider settings
SITE_ID = 1
# we must know our hostname for OIDC flow
SITE_URL = env('IDP_SITE_URL', default='http://127.0.0.1:7500')
if SITE_URL.endswith('/'):
    SITE_URL = SITE_URL[:-1]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
        },
        'sentry': {
            'handlers': ['console', 'sentry'],
            'propagate': False,
            'level': 'WARNING',
        },
    }
}


OIDC_EXTRA_SCOPE_CLAIMS = 'idp_core.extraclaims.AbnScopeClaims'
OIDC_IDTOKEN_EXPIRE = int(env("IDP_OIDC_IDTOKEN_EXPIRE", default=60 * 10))

SESSION_COOKIE_NAME = 'idp-testpoint'

RAVEN_DSN = env("IDP_RAVEN_DSN", default=None)

if RAVEN_DSN:
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# for django-storages library, to upload static files to S3
# this is pure deployment requirement, feel free to ignore it for local and gunicorn/uwsgi installations
AWS_STORAGE_BUCKET_NAME = env('IDP_AWS_STORAGE_BUCKET_NAME', default=None)
AWS_QUERYSTRING_AUTH = False
# it's safe to set 2099 here because if we change file content we change its name (hash part)
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
