# coding: utf-8

"""django informer commands"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from informer.checker.base import BaseInformer, InformerException


class Command(BaseCommand):
    help = 'Check all Informers.'

    def add_arguments(self, parser):
        # Positional
        # parser.add_argument('name', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--name',
            action='store_true',
            dest='name',
            default=False,
            help='A message help.')

    def handle(self, *args, **options):
        DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

        self.stdout.write('Checking Informers.')
        self.stdout.write('-' * 79)

        for namespace, classname in DJANGO_INFORMERS:
            try:
                cls = BaseInformer.get_class(namespace, classname)
                informer = cls()
                operational, message = informer.check()
            except InformerException as error:
                self.stderr.write('\n\t%s' % classname)
                self.stderr.write('\t\tmessage: %s' % error)
            except Exception as error:
                raise CommandError('A generic error occurred: %s' % error)
            else:
                self.stdout.write('\n\t%s' % classname)
                self.stdout.write('\t\toperational: %s' % operational)
                self.stdout.write('\t\tmessage: %s' % message)
