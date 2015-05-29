# coding: utf-8

"""informer tests for models"""

import mock
import pytest

from django.test import TestCase
from django.db import connections

from informer.models import BaseInformer, DatabaseInformer, InformerException


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

    def test_get_class_without_a_class(self):
        """
        A exception is raised, when the Informer in the settings does not
        exists
        """
        self.assertRaises(
            InformerException,
            BaseInformer.get_class, 'foo.models', 'BarInformer')

    def test_get_class_with_class_that_not_a_informer(self):
        """
        A exception is raised, when the Informer in the settings is not a
        Informer
        """
        self.assertRaises(
            InformerException,
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

        expected = (True, 'your database is operational')

        self.assertEqual(expected, informer.check())

    @mock.patch.object(connections['default'].introspection, 'table_names')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        informer = DatabaseInformer()

        m_mock.side_effect = Exception('Boom')

        self.assertRaises(InformerException, informer.check)
