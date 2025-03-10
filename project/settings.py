import os
from pathlib import Path
import environ
import sys
from urllib.parse import urlparse


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()

# Read the base .env file
env.read_env(os.path.join(BASE_DIR, '.env'))

# Determine which environment-specific .env file to load
environment = env('ENVIRONMENT')
env_file = (f'.env.{environment}')


if os.path.exists(env_file):
    # Load the environment file
    print(f"Loaded environment: {env_file}")
    env.read_env(env_file)
else:
    print(f"{env_file} file does not exist")
    sys.exit(1)




# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
print("DEBUG:", env("DEBUG"))
DEBUG = env.bool("DEBUG")


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'app.middleware.ServerRuntimeMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'

# Replace the DATABASES section of your settings.py with this
Postgres = urlparse(env("DATABASE_URL"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': Postgres.path.replace('/', ''),
        'USER': Postgres.username,
        'PASSWORD': Postgres.password,
        'HOST': Postgres.hostname,
        'PORT': 5432,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST framework settings
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'project.utils.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ]
}


ENV_CSRF_TRUSTED_ORIGINS =env("CSRF_TRUSTED_ORIGINS")
ENV_ALLOWED_HOSTS =env("ALLOWED_HOSTS")
ENV_CORS_ALLOWED_ORIGINS =env("CORS_ALLOWED_ORIGINS")
print("Trusted Origin:",ENV_CSRF_TRUSTED_ORIGINS.split(','))
print("Allowed Host:",ENV_ALLOWED_HOSTS.split(','))
print("Cors Allowed Origin:",ENV_CORS_ALLOWED_ORIGINS.split(','))


CSRF_TRUSTED_ORIGINS = ENV_CSRF_TRUSTED_ORIGINS.split(',')
ALLOWED_HOSTS = ENV_ALLOWED_HOSTS.split(',')
CORS_ALLOWED_ORIGINS = ENV_CORS_ALLOWED_ORIGINS.split(',')