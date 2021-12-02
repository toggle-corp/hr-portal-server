"""
Django settings for hr_portal project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APPS_DIR = os.path.join(BASE_DIR, 'apps')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]

# Application definition

INTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


THIRD_PARTY_APPS = [
    'rest_framework',
    'graphene_django',
    # 'graphene_django_extras',
    'graphene_graphiql_explorer',
    'drf_dynamic_fields',
    'corsheaders',
]


DEV_APPS = [
    'apps.user',
    'apps.leave',
]

INSTALLED_APPS = INTERNAL_APPS + THIRD_PARTY_APPS + DEV_APPS

GRAPHENE = {
    'ATOMIC_MUTATIONS': True,
    'SCHEMA': 'hr_portal.schema.schema',
    'SCHEMA_OUTPUT': 'schema.json',  # defaults to schema.json,
    'CAMELCASE_ERRORS': True,
    'SCHEMA_INDENT': 2,  # Defaults to None (displays all data on a single line)
    'MIDDLEWARE': [
        'utils.graphene.middleware.DisableIntrospectionSchemaMiddleware',
        'utils.sentry.SentryGrapheneMiddleware',
        'utils.graphene.middleware.WhiteListMiddleware',
    ],
}

GRAPHENE_DJANGO_EXTRAS = {
    'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.PageGraphqlPagination',
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 50,
}


GRAPHENE_NODES_WHITELIST = (
    '__schema',
    '__type',
    '__typename',
    # custom nodes...
    'login',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hr_portal.urls'

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

WSGI_APPLICATION = 'hr_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases\

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'PORT': os.environ['DATABASE_PORT'],
        'HOST': os.environ['DATABASE_HOST'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'user.User'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ['TIME_ZONE']

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = '/static'

    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS CONFIGS
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
# else:
#     CORS_ORIGIN_REGEX_WHITELIST = [
#         r"^https://192.168.88.12:3010$",
#     ]

# CORS_URLS_REGEX = r'(^/api/.*$)|(^/media/.*$)|(^/graphql$)'
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
