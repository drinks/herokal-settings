import re
import json
import sys
import io
from importlib import import_module
from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Serializes individual settings items into json-safe
              strings suitable for dumping into a .env for Foreman.'''

    option_list = BaseCommand.option_list + (
        make_option('--settings-module',
                    action='store',
                    dest='settings_module',
                    default='local_settings',
                    help='''The name of the local settings module to
                            export. Default is local_settings'''),
        make_option('--outfile',
                    action='store',
                    dest='outfile',
                    default='.env',
                    help='''The name of the file to write. Set to None
                            to print to stdout. Default is .env'''),
        make_option('--include-databases',
                    action='store_true',
                    dest='include_databases',
                    default=False,
                    help='''Whether or not to include the databases
                            dict in env output. Default is False.'''),
    )

    VALID_SETTING = re.compile(r'^[A-Z][A-Z0-9_]+$')

    def handle(self, *args, **options):
        flo = io.StringIO()
        failed_settings = []
        local_settings = import_module(options.get('settings_module'))
        settings_d = local_settings.__dict__
        for setting, value in settings_d.items():
            if not self.VALID_SETTING.search(setting):
                continue

            # Skip databases if not flagged to include them
            if setting == u"DATABASES" and not options.get('include_databases'):
                continue

            try:
                flo.write(u"%s=%s\n" % (setting, json.dumps(value, default=self.__class__._datehandler)))
            except Exception as e:
                failed_settings.append("%s: %s" % (setting, e))

        if options.get('outfile', 'None') != 'None':
            with open(options.get('outfile'), 'w+') as fp:
                fp.write(flo.getvalue())
        else:
            sys.stdout.write(flo.getvalue())
        if len(failed_settings):
            sys.stderr.write('\nFailed to parse some settings:\n')
            sys.stderr.write('\n'.join(failed_settings))

        flo.close()

    @staticmethod
    def _datehandler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))
