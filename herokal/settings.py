import os
import re
import json
import sys
import importlib


def apply_setting(setting, value, **kwargs):
    if re.search(r'^[A-Z][A-Z0-9_]+$', setting):
        if kwargs.get('parse_json') is True:
            try:
                setattr(sys.modules[__name__], setting, json.loads(value))
            except:
                setattr(sys.modules[__name__], setting, value)
        else:
            setattr(sys.modules[__name__], setting, value)


if 'DEBUG' in os.environ.keys():
    # Load .env file and
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(),
    }
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    for setting, value in os.environ.iteritems():
        apply_setting(setting, value, parse_json=True)
else:
    try:
        local_settings = importlib.import_module('..local_settings',
                                                 os.environ['DJANGO_SETTINGS_MODULE'])
        for name in dir(local_settings):
            apply_setting(name, getattr(local_settings, name))
    except ImportError as e:
        print("""Caught %s trying to import local_settings. Please make sure
                 local_settings.py exists and is free of errors.""")
        raise

try:
    del os
    del re
    del json
    del sys
    del local_settings
    del apply_setting
except:
    pass
