from .base import * # NOQA

DEBUG = True

INSTALLED_APPS += [
    # 'debug_toolbar',
    'silk',
    # 'raven.contrib.django.raven_compat',
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'POST': 3306,
    },
}

