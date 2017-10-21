from .settings import *

import os
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WSGI_APPLICATION = 'imeter24.wsgi.application'

SECRET_KEY = 'w_-jb%ek7yh7u5db74fl52d#u4#ro)mv(184^j68(sohpd7_j7'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'imeter24',
        'USER': 'role_imeter24',
        'PASSWORD': 'imeter24123',
        'HOST': '192.168.0.100',
        'PORT': '5432',
    }
}
