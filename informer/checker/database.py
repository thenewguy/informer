# coding: utf-8

"""
django informer checker for Database
"""

from django.db import (
    connection, Error, InterfaceError, DatabaseError, DataError,
    OperationalError, IntegrityError, InternalError, ProgrammingError,
    NotSupportedError)

from informer.checker.base import BaseInformer, InformerException
from informer.models import Raw


class DatabaseInformer(BaseInformer):
    """
    Database Informer.
    """

    def __str__(self):
        return u'Check if Database is operational.'

    def check_availability(self):
        """
        Inspect default database configuration.
        """
        try:
            Raw.objects.count()
        except (Error, InterfaceError, DatabaseError, DataError,
                OperationalError, IntegrityError, InternalError,
                ProgrammingError, NotSupportedError):
            return False, 'Oh no. Your database is out!'
        except Exception as error:
            raise InformerException(
                'An error occured when trying access database: %s' % error)
        else:
            return True, 'Your database is operational.'


class PostgresqlInformer(DatabaseInformer):
    """
    Extends default (Database Informer) and add PG stats.
    """

    def check_buffer(self):
        from random import randint

        result = randint(0, 100)

        query = """
            SELECT
                sum(heap_blks_read) / sum(heap_blks_hit) * 100 as TABLE,
                sum(idx_blks_read) / sum(idx_blks_hit) * 100 as INDEX,
                sum(toast_blks_read) / sum(toast_blks_hit) * 100 as TOAST,
                sum(tidx_blks_read) / sum(tidx_blks_hit) as TOASTIND
            FROM
                pg_statio_user_tables tables,
                (SELECT sum(blks_read) / sum(blks_hit) * 100 as SEQUENCE
                FROM pg_statio_user_sequences) sequences
            """

        #cursor = connection.cursor()
        #cursor.execute(query)
        #row = cursor.fetchone()

        return result, 'Check buffer: %s ' % result
