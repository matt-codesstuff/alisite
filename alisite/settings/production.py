import dj_database_url

from alisite.settings.common import *


DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
POSTGRES_PW = os.environ.get('POSTGRES_PW')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dfauc6hgt564k8',
        'USER': 'dfikrbvbkfbpkp',
        'PASSWORD': POSTGRES_PW,
        'HOST': 'ec2-44-215-40-87.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

WSGI_APPLICATION = 'alisite.wsgi.application'
