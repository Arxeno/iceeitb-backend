"""
Django settings for icee_backend2 project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.core.files.storage import Storage
from minio import Minio
from pathlib import Path
from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'iceeitb-backend.vercel.app',
    getenv('FE_URL')
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'register',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'icee_backend2.urls'

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

WSGI_APPLICATION = 'icee_backend2.wsgi.app'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'iceeitb',
#         'USER': 'iceeitb2024',
#         'PASSWORD': '8TkSis4QlmcV',
#         'HOST': 'ep-damp-darkness-98514520.ap-southeast-1.aws.neon.tech',
#         'PORT': '5432'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASS'),
        'HOST': getenv('DB_URL'),
        'PORT': '5432'
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

STATIC_URL = '/static/'
STATICFILES_DIRS = path.join(BASE_DIR, 'static'),
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles_build', 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False

#
# Google Drive Storage Settings
#

# GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = 'client_secrets.json'
# GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = 'uploads/'

# Environment variables
# AWS_ACCESS_KEY_ID = 'N7R31RQV4PJH0E2DGBKB'
# AWS_SECRET_ACCESS_KEY = 'c24aB8ygmW2rDYxDDF9PeLKvCFDLwHm66MADQ8d2'
# AWS_STORAGE_BUCKET_NAME = 'icee-storage'
# AWS_S3_SIGNATURE_NAME = 's3v4'
# AWS_S3_REGION_NAME = getenv('AWS_S3_REGION_NAME')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_VERITY = True

# settings.py

# Import the necessary libraries

# Custom storage backend using MinIO


# class S3CompatibleStorage(Storage):
#     def __init__(self, endpoint, access_key, secret_key, secure=True, bucket_name=None):
#         self.endpoint = endpoint
#         self.access_key = access_key
#         self.secret_key = secret_key
#         self.secure = secure
#         self.bucket_name = bucket_name

#     def _open(self, name, mode='rb'):
#         # Implement opening files from the storage
#         # You can use the MinIO Python library to interact with the storage here
#         pass

#     def _save(self, name, content):
#         # Implement saving files to the storage
#         # You can use the MinIO Python library to interact with the storage here
#         pass

#     def url(self, name):
#         # Generate a URL for accessing the file in the storage
#         # You can use the MinIO Python library to generate the URL here
#         pass

# # Configure the S3-compatible storage backend
# S3_COMPATIBLE_STORAGE_ENDPOINT = 'https://is3.cloudhost.id'
# S3_COMPATIBLE_STORAGE_ACCESS_KEY = 'N7R31RQV4PJH0E2DGBKB'
# S3_COMPATIBLE_STORAGE_SECRET_KEY = 'c24aB8ygmW2rDYxDDF9PeLKvCFDLwHm66MADQ8d2'
# S3_COMPATIBLE_STORAGE_BUCKET_NAME = 'icee-storage'

# AWS_ACCESS_KEY_ID = 'N7R31RQV4PJH0E2DGBKB'
# AWS_SECRET_ACCESS_KEY = 'c24aB8ygmW2rDYxDDF9PeLKvCFDLwHm66MADQ8d2'
# AWS_STORAGE_BUCKET_NAME = 'icee-storage'
# AWS_S3_ENDPOINT_URL = 'https://is3.cloudhost.id/'
# AWS_S3_CUSTOM_DOMAIN = None

# DEFAULT_FILE_STORAGE = 'icee_backend2.settings.S3CompatibleStorage'

# Environment variables
# AWS_ACCESS_KEY_ID = 'N7R31RQV4PJH0E2DGBKB'
# AWS_SECRET_ACCESS_KEY = 'c24aB8ygmW2rDYxDDF9PeLKvCFDLwHm66MADQ8d2'
# AWS_STORAGE_BUCKET_NAME = 'icee-storage'
# AWS_S3_SIGNATURE_NAME = 's3v4'
# AWS_S3_REGION_NAME = getenv('AWS_S3_REGION_NAME')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_VERITY = True
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MINIO_ENDPOINT = 'is3.cloudhost.id'
MINIO_ACCESS_KEY = 'N7R31RQV4PJH0E2DGBKB'
MINIO_SECRET_KEY = 'c24aB8ygmW2rDYxDDF9PeLKvCFDLwHm66MADQ8d2'
MINIO_BUCKET_NAME = 'icee-storage'

DEFAULT_FILE_STORAGE = 'register.custom_storage.MinioStorage'
DJANGO_DOMAIN = getenv('DJANGO_DOMAIN')
