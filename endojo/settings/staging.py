from endojo.settings.base import *
import secrets

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    'dev.endojo.hama.sh',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets.dev_db_dbname,
        'USER': secrets.dev_db_username,
        'PASSWORD': secrets.dev_db_password,
        'HOST': secrets.dev_db_hostname,
        'PORT': secrets.dev_db_port,
    }
}
