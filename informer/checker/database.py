# coding: utf-8

"""
django informer checker for Database
"""

from django.conf import settings
from django.db import connections

from informer.checker.base import BaseInformer, InformerException
from informer.models import Raw


class DatabaseInformer(BaseInformer):
    """
    Database Informer.
    """

    def __str__(self):
        return u'Check if Database is operational.'

    def check(self):
        """
        Inspect default database configuration.
        """
        try:
            conn = connections['default']
            conn.introspection.table_names()
        except Exception as error:
            raise InformerException(
                'An error occured when trying access database: %s' % error)
        else:
            return True, 'Your database is operational.'

    def check_latency(self):
        return 'LATENCY ---------- ', 10