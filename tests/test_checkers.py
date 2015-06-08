# coding: utf-8

"""informer tests for checkers"""

import mock
import pytest

from django.test import TestCase
from django.db import connections
from django.conf import settings

from informer.checker.base import BaseInformer, InformerException
from informer.checker.database import DatabaseInformer
from informer.checker.storage import StorageInformer
from informer.checker.celery import CeleryInformer


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

    def test_check(self):
        """
        Test if 'check' raises a NotImplementedError
        """
        informer = BaseInformer()
        self.assertRaises(NotImplementedError, informer.check)

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

    @mock.patch('__builtin__.__import__')
    def test_get_class_failure(self, m_import):
        """
        Test if exception handling works when a generic error occurs
        """
        m_import.side_effect = Exception('Cataploft')

        self.assertRaises(
            Exception,
            BaseInformer.get_class, 'tests.test_checker.', 'BarInformer')


class DatabaseInformerTest(TestCase):
    """
    Tests to Database Informer
    """

    def test_unicode(self):
        """
        Test if Unicode is correctly specified
        """
        informer = DatabaseInformer()
        expected = u'Check if database is operational.'
        self.assertEqual(expected, str(informer))

    def test_check(self):
        """
        Test if with 'ideal scenario', all goes fine
        """
        informer = DatabaseInformer()

        expected = (True, 'Your database is operational.')

        self.assertEqual(expected, informer.check())

    @mock.patch.object(connections['default'].introspection, 'table_names')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        informer = DatabaseInformer()

        m_mock.side_effect = Exception('Boom')

        self.assertRaises(InformerException, informer.check)


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

        self.assertEqual(expected, informer.check())

    @mock.patch('django.core.files.storage.Storage.save')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.side_effect = Exception('Boom')

        informer = StorageInformer()

        self.assertRaises(InformerException, informer.check)


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
    def test_check(self, mock):
        """
        Test if with 'ideal scenario', all goes fine
        """
        mock.stats.return_value = { 'foo': 'bar '}
        informer = CeleryInformer()

        expected = (True, 'Celery is operational.')

        self.assertEqual(expected, informer.check())

    @mock.patch('celery.app.control.Control.inspect')
    def test_check_task_fail(self, mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        mock().stats.return_value = None

        informer = CeleryInformer()

        expected = (False, 'No running Celery workers were found.')

        self.assertEqual(expected, informer.check())

    @mock.patch('celery.app.control.Control.inspect')
    def test_check_exceptions(self, mock):
        """
        Test if with 'broken scenario', all goes bad
        """

        # TODO: Fragment into various methods and check messages.

        informer = CeleryInformer()

        with self.assertRaises(InformerException):
            mock.side_effect = IOError('Boom')
            informer.check()

        with self.assertRaises(InformerException):
            mock.side_effect = ImportError('Boom')
            informer.check()

        with self.assertRaises(InformerException):
            mock.side_effect = Exception('Boom')
            informer.check()
