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
        #  logger.info('Starting PostgreSQL check')

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
    """

    def check_size(self):
        #  logger.info('Collecting Database Stats')

        cursor = connection.cursor()

        database = settings.DATABASES.get('default')
        name = database.get('NAME')
        engine = database.get('ENGINE')

        if engine != 'django.db.backends.postgresql_psycopg2':
            return 0, 'Default database is not Postgres'

        query = self.query_database_stats(name)
        cursor.execute(query)

        db, size, commit, rollback, read, hit = cursor.fetchone()

        return size, 'database size on %s' % datetime.now()

    def query_table_stats(self):
        return """
        /* # noqa */
        SELECT
            psut.schemaname,
            pc.relname,
            pg_table_size(pc.relname::varchar) tblsize,
            pg_indexes_size(pc.relname::varchar) idxsize,
            pg_total_relation_size(pc.relname::varchar) relsize,
            pc.reltuples::bigint,
            pc.relpages,
            coalesce(round((8192 / (nullif(pc.reltuples, 0) / nullif(pc.relpages, 0)))), 0) avg_tuplesize,
            psut.seq_scan,
            psut.idx_scan,
            coalesce(100 * psut.idx_scan / nullif((psut.idx_scan + psut.seq_scan), 0), 0)::int per_idx_scan,
            coalesce(100 * psiout.heap_blks_hit / nullif((psiout.heap_blks_hit + psiout.heap_blks_read), 0), 0)::int per_rel_hit,
            coalesce(100 * psiout.idx_blks_hit / nullif((psiout.idx_blks_hit + psiout.idx_blks_read), 0), 0)::int per_idx_hit,
            psut.n_tup_ins,
            psut.n_tup_upd,
            psut.n_tup_hot_upd,
            coalesce(100 * psut.n_tup_hot_upd / nullif(psut.n_tup_upd, 0), 0)::int per_hot_upd,
            psut.n_tup_del,
            psut.n_live_tup,
            psut.n_dead_tup,
            coalesce(100 * psut.n_dead_tup / nullif(psut.n_live_tup, 0), 0)::int per_deadfill
        FROM
            pg_stat_user_tables psut
            INNER JOIN pg_statio_user_tables psiout ON psiout.relname = psut.relname
            INNER JOIN pg_class pc ON pc.relname = psut.relname
        ORDER BY
            pc.relname asc
        """

    def query_index_stats(self):
        return """
        /* # noqa */
        SELECT
            pi.schemaname,
            pcr.relname as relname,
            pci.relname as idxname,
            pg_size_pretty(pg_total_relation_size(pci.relname::varchar)) idxsize_pret,
            pg_total_relation_size(pci.relname::varchar) idxsize,
            pci.reltuples::bigint idxtuples,
            pcr.reltuples::bigint reltuples,
            coalesce(100 * pci.reltuples / nullif(pcr.reltuples, 0), 0)::int per_idx_covered,
            pi.idx_scan,
            pi.idx_tup_read,
            pi.idx_tup_fetch
        FROM
            pg_stat_user_indexes pi
        INNER JOIN pg_class pci ON pci.oid = pi.indexrelid
        INNER JOIN pg_class pcr ON pcr.oid = pi.relid
        ORDER BY
            schemaname, relname, idxname
        """

    def query_function_stats(self):
        return """
        SELECT
            schemaname,
            funcname,
            calls,
            self_time,
            total_time
        FROM
            pg_stat_user_functions
        WHERE
            schemaname <> 'pg_catalog'
        """

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

    def query_connections(self, database):
        return """
        SELECT
            count(1) connections
        FROM
            pg_stat_activity() where datname = '%s'
        """ % (database)

    def query_waiting_connections(self, database):
        return """
        SELECT
            count(1) waiting_connections
        FROM
            pg_stat_activity()
        WHERE
            waiting is true and datname = '%s'
        """ % (database)

    def query_replication_delay(self):
        return """
        /* # noqa */
        SELECT extract(epoch from (now() - pg_last_xact_replay_timestamp())) * 1000 as replication_delay
        """

    def query_heap_memory_stats(self):
        return """
        /* # noqa */
        SELECT
            cast(sum(heap_blks_read) as bigint) heap_read,
            cast(sum(heap_blks_hit) as bigint) heap_hit,
            coalesce(cast(sum(heap_blks_hit) / nullif((sum(heap_blks_hit) + sum(heap_blks_read)), 0) * 100 as bigint), 0)::int per_heap_ratio
        FROM
            pg_statio_user_tables
        """

    def query_index_memory_stats(self):
        return """
        /* # noqa */
        SELECT
            cast(sum(idx_blks_read) as bigint) idx_read,
            cast(sum(idx_blks_hit) as bigint) idx_hit,
            coalesce(cast(sum(idx_blks_hit) / nullif((sum(idx_blks_hit) + sum(idx_blks_read)), 0) * 100 as bigint), 0)::int per_idx_ratio
        FROM
            pg_statio_user_indexes
        """
