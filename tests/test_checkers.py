# coding: utf-8

"""
Informer tests for checkers
"""

import mock
import pytest

from django.test import TestCase
from django.core.cache import cache
from django.db import DatabaseError

from informer.checker.base import BaseInformer, InformerException
from informer.checker.database import DatabaseInformer, PostgresqlInformer
from informer.checker.storage import StorageInformer
from informer.checker.celery import CeleryInformer
from informer.checker.cache import CacheInformer

from informer.models import Raw


pytestmark = pytest.mark.django_db


class BarInformer(object):
    """
    A class to help with tests
    """
    pass


class BaseInformerTest(TestCase):
    """
    Tests to Base Class
    """

    def test_unicode(self):
        """
        Test if Unicode is correctly specified
        """
        informer = BaseInformer()
        expected = u'A small and explicit description from informer.'
        self.assertEqual(expected, str(informer))

    def test_check_availability(self):
        """
        Test if 'check' raises a NotImplementedError
        """
        informer = BaseInformer()

        self.assertRaises(NotImplementedError, informer.check_availability)

    def test_get_class(self):
        """
        Test if 'get_class' can instantiate a Informer
        """
        cls = BaseInformer.get_class(
            'informer.checker.database', 'DatabaseInformer')

        informer = cls()

        expected = isinstance(informer, (BaseInformer, DatabaseInformer))

        self.assertTrue(expected)

    def test_get_class_without_class_on_namespace(self):
        """
        Test if exception handling works when class does not exists on
        namespace
        """
        self.assertRaises(
            InformerException,
            BaseInformer.get_class, 'informer.models', 'BarInformer')

    def test_get_class_with_unknown_class(self):
        """
        Test if exception handling works when an Informer is unknown
        """
        self.assertRaises(
            InformerException,
            BaseInformer.get_class, 'foo.models', 'BarInformer')

    def test_get_class_with_class_that_not_a_informer(self):
        """
        Test if exception handling works when an Informer does not inherit from
        BaseInformer
        """
        self.assertRaises(
            InformerException,
            BaseInformer.get_class, 'tests.test_checkers', 'BarInformer')

    @mock.patch('informer.checker.base.import_module')
    def test_get_class_failure(self, m_import):
        """
        Test if exception handling works when a generic error occurs
        """
        m_import.side_effect = Exception('Cataploft')

        self.assertRaises(
            Exception,
            BaseInformer.get_class, 'tests.test_checkers', 'BarInformer')


class DatabaseInformerTest(TestCase):
    """
    Tests to Database Informer
    """

    def test_unicode(self):
        """
        Test if Unicode is correctly specified
        """
        informer = DatabaseInformer()
        expected = u'Check if Database is operational.'
        self.assertEqual(expected, str(informer))

    def test_check_availability(self):
        """
        Test if with 'ideal scenario', all goes fine
        """
        informer = DatabaseInformer()

        expected = (True, 'Your database is operational.')

        self.assertEqual(expected, informer.check_availability())

    @mock.patch.object(Raw.objects, 'count')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        informer = DatabaseInformer()

        m_mock.side_effect = Exception('Boom')

        self.assertRaises(InformerException, informer.check_availability)

    @mock.patch.object(Raw.objects, 'count')
    def test_check_fails_when_database_is_broken(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        informer = DatabaseInformer()

        m_mock.side_effect = DatabaseError('Boom')

        expected = (False, 'Oh no. Your database is out!')

        self.assertEqual(expected, informer.check_availability())


class PostgresqlInformerTest(TestCase):
    """
    Tests to PostgreSQL Informer
    """
    def test_check_availability(self):
        """
        Test if with 'ideal scenario', all goes fine
        """
        informer = PostgresqlInformer()

        expected = (True, 'Your database is operational.')

        self.assertEqual(expected, informer.check_availability())

        print(Raw.objects.all())


class StorageInformerTest(TestCase):
    """
    Tests to Storage Informer.
    """

    def test_unicode(self):
        """
        Test if Unicode is correctly specified.
        """
        informer = StorageInformer()
        expected = u'Check if Storage is operational.'
        self.assertEqual(expected, str(informer))

    def test_check(self):
        """
        Test if with 'ideal scenario', all goes fine
        """
        informer = StorageInformer()

        expected = (True, 'Your FileSystemStorage is operational.')

        self.assertEqual(expected, informer.check_availability())

    @mock.patch('django.core.files.storage.Storage.save')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.side_effect = Exception('Boom')

        informer = StorageInformer()

        self.assertRaises(InformerException, informer.check_availability)


class CeleryInformerTest(TestCase):
    """
    Tests to Celery Informer.
    """

    def test_unicode(self):
        """
        Test if Unicode is correctly specified.
        """
        informer = CeleryInformer()
        expected = u'Check if Celery is operational.'
        self.assertEqual(expected, str(informer))

    @mock.patch('celery.app.control.Control.inspect')
    def test_check_availability(self, mock):
        """
        Test if with 'ideal scenario', all goes fine
        """
        mock.stats.return_value = {'foo': 'bar '}
        informer = CeleryInformer()

        expected = (True, 'Celery is operational.')

        self.assertEqual(expected, informer.check_availability())

    @mock.patch('celery.app.control.Control.inspect')
    def test_check_task_fail(self, mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        mock().stats.return_value = None

        informer = CeleryInformer()

        expected = (False, 'No running Celery workers were found.')

        self.assertEqual(expected, informer.check_availability())

    @mock.patch('celery.app.control.Control.inspect')
    def test_check_exceptions(self, mock):
        """
        Test if with 'broken scenario', all goes bad
        """

        # TODO: Fragment into various methods and check messages.

        informer = CeleryInformer()

        with self.assertRaises(InformerException):
            mock.side_effect = IOError('Boom')
            informer.check_availability()

        with self.assertRaises(InformerException):
            mock.side_effect = ImportError('Boom')
            informer.check_availability()

        with self.assertRaises(InformerException):
            mock.side_effect = Exception('Boom')
            informer.check_availability()


class CacheInformerTest(TestCase):
    """
    Tests to Cache Informer
    """

    def test_unicode(self):
        """
        Test if Unicode is correctly specified
        """
        informer = CacheInformer()
        expected = u'Check if Cache is operational.'
        self.assertEqual(expected, str(informer))

    def test_check(self):
        """
        Test if with 'ideal scenario', all goes fine
        """
        informer = CacheInformer()

        expected = (True, 'Your cache system is operational.')

        self.assertEqual(expected, informer.check_availability())

    @mock.patch.object(cache, 'get')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        informer = CacheInformer()

        m_mock.side_effect = Exception('Boom')

        self.assertRaises(InformerException, informer.check_availability)
