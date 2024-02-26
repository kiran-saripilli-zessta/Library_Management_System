from pathlib import Path
import zoneinfo
import os
from storages.backends.s3boto3 import S3Boto3Storage


zoneinfo.available_timezones()



BASE_DIR = Path(__file__).resolve().parent.parent





# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$y7wok$@25=32c2sl&dy_%w%yo3=okhghbwtc7g1*@xu(1a$q1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'LibManagSys',
    'libxmApp',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'import_export',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'middleware.main.CheckBookAvailabilityMiddleware',
    'middleware.main.CurrentUserMiddleware',
    
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

ROOT_URLCONF = 'LibManagSys.urls'

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

WSGI_APPLICATION = 'LibManagSys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


APP_LOG_FILENAME = os.path.join(BASE_DIR, 'log/app.log')
ERROR_LOG_FILENAME = os.path.join(BASE_DIR, 'log/error.log')
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    BASE_DIR / 'libxmApp' / 'static' 
]

STATIC_ROOT = BASE_DIR / 'assets'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRONJOBS = [
    ('*/5 * * * *', 'libxmApp.cron.print_hello')
]


AWS_ACCESS_KEY_ID = 'AKIAYH6OSFREV5YC3LWZ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'libraryuserimages'
AWS_REGION = 'ap-south-1'
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'



# Only public read for now
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'