================
herokal-settings
================

Provides crosswalk between a Foreman-style .env file and your
django local settings.


Installation & Usage
--------------------

Add to your django project's requirements.txt::

    herokal-settings

Add `herokal` to `INSTALLED_APPS`

Install the heroku-config plugin::

    heroku plugins:install git://github.com/ddolar/heroku-config.git

Run the management command to export your local_settings.py::

    ./manage.py exportenv

At the bottom of your settings.py, instead of::

    from local_settings import *

Use herokal.settings::

    from herokal.settings import *

Now, when you run ./manage.py runserver, your `local_settings.py` will be loaded,
but when you run `foreman start`, your `.env` will be used.

Options
-------

The `exportenv` command takes a few optional flags::

    --settings-module           The name of the settings module to export.
                                Default is 'local_settings'

    --include-databases         Whether or not to serialize database
                                connections into the .env file.
                                Default is false

    --outfile                   The name of the file to export your
                                local settings to.
                                Default is '.env'


Changelog
---------

**0.0.1**

* Initial release
