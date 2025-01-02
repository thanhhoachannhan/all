
import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


load_dotenv()

""" Base settings """
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv("DEBUG") == "True" or True
SECRET_KEY = 'DJANGO'
ALLOWED_HOSTS=['*']
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

#-------------------------------------------------
# APPS
#-------------------------------------------------
APPS = [
    'authentication', 'core', 'ts',
    'ecommerce', 'marketplace'
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_htmx'
]
INSTALLED_APPS = DJANGO_APPS + THIRTY_APPS + [app for app in APPS]

AUTH_USER_MODEL = 'authentication.User'

# Process: Inactive Errors messagse when login
AUTHENTICATION_BACKENDS = ['authentication.backends.AuthenticationBackend']

#-------------------------------------------------
# Media
#-------------------------------------------------
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

#-------------------------------------------------
# Templates
#-------------------------------------------------
CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages'
]
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': CONTEXT_PROCESSORS,},
}]

#-------------------------------------------------
# Databases
#-------------------------------------------------
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#-------------------------------------------------
# Timezone
#-------------------------------------------------
USE_TZ = True
USE_L10N = True
TIME_ZONE = 'UTC'

#-------------------------------------------------
# Languages
#-------------------------------------------------
USE_I18N = True
LANGUAGE_CODE = 'en'
LOCALE_PATHS = [BASE_DIR / 'locale/',]
LANGUAGES = (
    ('en', _('English')),
    ('vi', _('Vietnamese')),
    ('ja', _('Japanese')),
)
if not os.path.exists(BASE_DIR / 'locale'): os.mkdir('locale')
for lang in LANGUAGES:
    if not os.path.exists(BASE_DIR / 'locale' / lang[0]): os.mkdir(BASE_DIR / 'locale' / lang[0])
    if not os.path.exists(BASE_DIR / 'locale' / lang[0] / 'LC_MESSAGES'): os.mkdir(BASE_DIR / 'locale' / lang[0] / 'LC_MESSAGES')

#-------------------------------------------------
# Email
#-------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FOLDER_NAME = 'emails'
EMAIL_FILE_PATH = BASE_DIR / EMAIL_FOLDER_NAME
if not os.path.exists(EMAIL_FILE_PATH): os.mkdir(EMAIL_FOLDER_NAME)
if not os.path.exists(EMAIL_FILE_PATH/'.gitkeep'):
    f = open(EMAIL_FILE_PATH/'.gitkeep', 'w')
    f.close()

#-------------------------------------------------
# Middleware
#-------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware', # for django htmx
    'authentication.middleware.BlockLocalUserMiddleware', # Fix: Cannot query "None(User)": Must be "Group" instance.
]

""" Redirect """
LOGIN_URL = '/authentication/login/'
""" Extra """
PASSWORD_RESET_TIMEOUT = 60 # thoi gian hen han cua token tao ra tu default_token_generator
USER_TYPE_CHOICES = (
    ('global', 'Global User'),
    ('ecommerce', 'Ecommerce App User'),
    ('test', 'Test App User'),
    ('marketplace', 'Marketplace App User'),
) # su dung cho truong hop nhieu loai user 

#-------------------------------------------------
# Rest Framework
#-------------------------------------------------
APPEND_SLASH = False
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5000),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=100),
}

#-------------------------------------------------
# Logging
#-------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
    },
}

""" Celery """
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Địa chỉ của Redis broker
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Địa chỉ của Redis backend
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'print-hello-world': {
        'task': 'project.celery.task_one',
        'schedule': 5,  # Lặp lại mỗi 5 giây
    },
}
""" EOF """
