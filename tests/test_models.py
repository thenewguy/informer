# coding: utf-8

"""informer tests for models"""

import mock
import pytest

from django.test import TestCase
from django.db import connections
from django.conf import settings

from informer.models import BaseInformer, DatabaseInformer, InformerException
from informer.models import StorageInformer, CeleryInformer


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
        cls = BaseInformer.get_class('informer.models', 'DatabaseInformer')

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
            BaseInformer.get_class, 'tests.test_models.', 'BarInformer')

    @mock.patch('__builtin__.__import__')
    def test_get_class_failure(self, m_import):
        """
        Test if exception handling works when a generic error occurs
        """
        m_import.side_effect = Exception('Cataploft')

        self.assertRaises(
            Exception,
            BaseInformer.get_class, 'tests.test_models.', 'BarInformer')


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

    def test_check(self):
        """
        Test if with 'ideal scenario', all goes fine
        """
        informer = CeleryInformer()

        expected = (True, 'Celery is operational.')

        self.assertEqual(expected, informer.check())

    @mock.patch.object(settings, 'INSTALLED_APPS')
    def test_missing_configuration(self, m_mock):
        mock.return_value = []

        informer = CeleryInformer()

        self.assertRaises(InformerException, informer.check)

    @mock.patch('celery.result.EagerResult.successful')
    def test_check_task_fail(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.return_value = False

        informer = CeleryInformer()

        expected = (False, 'Celery is out.')

        self.assertEqual(expected, informer.check())

    @mock.patch('django.conf.settings.INSTALLED_APPS')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.side_effect = Exception('Boom')

        informer = CeleryInformer()

        self.assertRaises(InformerException, informer.check)

    @mock.patch('celery.task.task')
    def test_check_failure_if_celery_is_missing(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.side_effect = ImportError('Boom')

        informer = CeleryInformer()

        self.assertRaises(InformerException, informer.check)
