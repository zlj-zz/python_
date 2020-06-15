from .base import * # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGING': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
