from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = ['*']

# Se puede usar otra base de datos como PostgreSQL, MySQL, etc.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
