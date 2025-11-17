from .base import *

DEBUG = True

# Database locale pour développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='publications_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# CORS permissif en dev
CORS_ALLOW_ALL_ORIGINS = True

# Email backend pour développement (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'