# coding: utf-8

"""
django informer checker for Database
"""

import logging
from datetime import datetime

from django.conf import settings
from django.db import (
    connection, Error, InterfaceError, DatabaseError, DataError,
    OperationalError, IntegrityError, InternalError, ProgrammingError,
    NotSupportedError)

from informer.checker.base import BaseInformer, InformerException
from informer.models import Raw


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


class PostgresInformer(DatabaseInformer):
    """
    Extends default (Database Informer) and add PG stats.

    The queries and some insights, started from this gist:
    https://gist.github.com/robertsosinski/6345564
    """

    def _execute_query(self, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            raise e
        else:
            return cursor.fetchone()
        finally:
            cursor.close()

    def check_size(self):
        database = settings.DATABASES.get('default')
        name = database.get('NAME')
        query = self.query_database_stats(name)

        try:
            db, size, commit, rollback, read, hit = self._execute_query(query)
        except (Error, InterfaceError, DatabaseError, DataError,
                OperationalError, IntegrityError, InternalError,
                ProgrammingError, NotSupportedError) as db_error:
            return 0, 'We can not get the database size (%s).' % db_error
        except Exception as error:
            raise InformerException(
                'An error occured when trying access database: %s' % error)
        else:
            return size, 'database size on %s' % datetime.now()

    def query_database_stats(self, database):
        return """
        SELECT
            datname,
            pg_database_size('%s') db_size,
            xact_commit,
            xact_rollback,
            blks_read,
            blks_hit
        FROM
            pg_stat_database
        WHERE
            datname = '%s'
        """ % (database, database)
