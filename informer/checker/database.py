# coding: utf-8

"""
django informer checker for Database
"""

from django.conf import settings
from django.db import connections

from informer.checker.base import BaseInformer, InformerException


def collect_metrics(check):
    def wrapper(*args, **kwargs):
        print 'generate raw data'

        return check(*args, **kwargs)

    return wrapper


class DatabaseInformer(BaseInformer):
    """
    Database Informer.
    """

    def __str__(self):
        return u'Check if Database is operational.'

    def inspect(self, check):
        def wrapper(*args, **kwargs):
            print 'INSPECT ------- '

        return check(*args, **kwargs)

        return wrapper

    @inspect
    def check(self):
        """
        Inspect default database configuration.
        """
        print '\n\n', ':: Perform Checking'
        print '-' * 100

        try:
            conn = connections['default']
            conn.introspection.table_names()
        except Exception as error:
            raise InformerException(
                'An error occured when trying access database: %s' % error)
        else:
            return True, 'Your database is operational.'
