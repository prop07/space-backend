import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load SECRET_KEY, DEBUG, and other values from the environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-+5ksi1yq6tq5e(o^@(h-*eft_fyx-@uixo-0-%jjg=g-rb3)&w')
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Convert DEBUG to boolean

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Load additional environment variables for EC2 connection and superuser credentials
KEY_FILE = os.getenv('KEY_FILE', '/path/to/your/key.pem')
USER = os.getenv('USER', 'ec2-user')
HOST = os.getenv('HOST', 'your-ec2-instance-ip-or-dns')
SUPERUSER_EMAIL = os.getenv('SUPERUSER_EMAIL', 'prop@gmail.com')
SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD', 'prop')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # app
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
    # middleware
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

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'EXCEPTION_HANDLER': 'project.utils.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ]
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://frontend-domain.com",
]

# Additional config (for EC2 connection and superuser management, if needed)
# Example:
# print(f"Connecting to EC2 instance {USER}@{HOST} using key file {KEY_FILE}")
