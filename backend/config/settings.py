"""Настройки Django-приложения Trenly."""

import os
from pathlib import Path
from urllib.parse import unquote, urlparse

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Ключ из .env.example. Допустим только при DEBUG=1.
LOCAL_INSECURE_SECRET_KEY = 'dev-only-insecure-secret-key'


def load_env_file(path: Path) -> None:
    """Подмешивает KEY=VALUE из файла, не перезаписывая уже заданное окружение."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line.removeprefix('export ').strip()
        key, separator, value = line.partition('=')
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


def env_flag(name: str, default: str = '0') -> bool:
    return os.environ.get(name, default).strip().lower() in {'1', 'true', 'yes', 'on'}


def database_from_url(url: str) -> dict:
    parsed = urlparse(url)
    if parsed.scheme not in {'postgres', 'postgresql'}:
        raise ImproperlyConfigured('DATABASE_URL должен быть адресом PostgreSQL.')
    name = unquote(parsed.path.lstrip('/'))
    if not name:
        raise ImproperlyConfigured('DATABASE_URL должен содержать имя базы.')
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': unquote(parsed.username) if parsed.username else '',
        'PASSWORD': unquote(parsed.password) if parsed.password else '',
        'HOST': parsed.hostname or '',
        'PORT': str(parsed.port or ''),
    }


load_env_file(BASE_DIR / '.env')

DEBUG = env_flag('DEBUG')
SECRET_KEY = os.environ.get('SECRET_KEY', LOCAL_INSECURE_SECRET_KEY)
if not DEBUG and SECRET_KEY == LOCAL_INSECURE_SECRET_KEY:
    raise ImproperlyConfigured(
        'Без DEBUG приложение не стартует с SECRET_KEY из примера. '
        'Задайте свой SECRET_KEY.'
    )

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'config',
    'trainers',
    'clients',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if not DATABASE_URL:
    raise ImproperlyConfigured('Задайте DATABASE_URL.')
DATABASES = {'default': database_from_url(DATABASE_URL)}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

TRAINER_PHOTO_ROOT = Path(os.environ.get('TRAINER_PHOTO_ROOT', BASE_DIR / 'media' / 'trainer-photos'))

_object_storage_endpoint = os.environ.get('OBJECT_STORAGE_ENDPOINT', '').strip()
if _object_storage_endpoint:
    AWS_S3_ENDPOINT_URL = _object_storage_endpoint
    AWS_STORAGE_BUCKET_NAME = os.environ['OBJECT_STORAGE_BUCKET']
    AWS_S3_ACCESS_KEY_ID = os.environ.get('OBJECT_STORAGE_ACCESS_KEY', '')
    AWS_S3_SECRET_ACCESS_KEY = os.environ.get('OBJECT_STORAGE_SECRET_KEY', '')
    AWS_S3_FILE_OVERWRITE = True
    AWS_DEFAULT_ACL = 'private'
    AWS_QUERYSTRING_AUTH = True
    _trainer_photo_storage = {'BACKEND': 'storages.backends.s3.S3Storage'}
else:
    _trainer_photo_storage = {'BACKEND': 'trainers.storage.TrainerPhotoFileStorage'}

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    'trainer_photos': _trainer_photo_storage,
}

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Trenly API',
    'DESCRIPTION': 'API кабинета тренера.',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
