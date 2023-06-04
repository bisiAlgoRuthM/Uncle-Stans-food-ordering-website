import os
import django

from django.conf import settings
from main.models import MenuItem

settings.configure(
    DEBUG=True,  # Set your desired debug mode
    SECRET_KEY='django-insecure-xe=yh@&4ydt&x5zr@jdwp8%i7x69&t#x#^)cy=unv6m32z0=sy',  # Set your secret key
    INSTALLED_APPS=[
        'main',  # Add your Django app to the installed apps
        # Add other installed apps if necessary
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
)





