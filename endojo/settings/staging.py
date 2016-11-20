from endojo.settings.base import *
import secrets

DEBUG = False

AWS_STORAGE_BUCKET_NAME = 'endojo-staging'

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
