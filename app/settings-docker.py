from app.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bidder',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

MEDIA_ROOT = '/home'

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0
