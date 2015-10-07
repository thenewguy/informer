# coding: utf-8

"""
django informer checker for Database
"""

from django.conf import settings
from django.db import connections

from informer.checker.base import BaseInformer, InformerException
from informer.models import Raw


def collect(func):
    """
    Collect metrics.
    """

    def wrapper(instance, *args, **kwargs):
        instance._collect_metrics()
        return func(instance)

    return wrapper


class DatabaseInformer(BaseInformer):
    """
    Database Informer.
    """

    def __str__(self):
        return u'Check if Database is operational.'

    @collect
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

    def _collect_metrics(self):
        """
        'Discovery' of the methods that collect the metrics of this informer.
        """
        collectors = [c for c in dir(self) if c.startswith('_collect_')]

        for collector in collectors:
            getattr(self, collector, None)()

    def _collect_uptime(self):
        print '-' * 5, 'UPTIME', '-' * 5
        #Raw.objects.get_or_create(
        #    indicator=self.__class__.__name__, measure='uptime', value=True)

