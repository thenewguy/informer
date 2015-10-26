# coding: utf-8

"""
informer tests for views
"""

import mock
import json
import pytest

from django.test import TestCase, Client
from django.db import connections

from informer.models import Raw
from informer.factories import RawFactory

pytestmark = pytest.mark.django_db


class DefaultViewTest(TestCase):
    """
    Tests to Default View
    """

    def test_get(self):
        """
        Test if web app is ok
        """
        client = Client()

        response = client.get('/')

        self.assertEqual(200, response.status_code)


class DiscoverViewTest(TestCase):
    """
    Tests responses from Informer Discover
    """

    def test_get(self):
        """
        Test if 'discover' has a list with all informer registered
        """
        client = Client()

        response = client.get('/discover/')

        self.assertEqual(200, response.status_code)

        result = json.loads(response.content.decode())

        expected = {
            u'informers': [{
                u'url': u'/database/',
                u'name': u'database'
            }, {
                u'url': u'/storage/',
                u'name': u'storage'
            }, {
                u'url': u'/celery/',
                u'name': u'celery'
            }, {
                u'url': u'/cache/',
                u'name': u'cache'
            }]
        }

        self.assertEqual(expected, result)


class InformerViewTest(TestCase):
    """
    Tests responses from Informer details
    """

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """
        Test if 'details' from a specific Informer has a expected data
        """

        response = self.client.get('/database/')

        self.assertEqual(200, response.status_code)

        result = json.loads(response.content.decode())

        expected = {
            u'message': u'Your database is operational.',
            u'name': u'DatabaseInformer',
            u'operational': True,
            u'measures': [u'availability']
        }

        self.assertEqual(expected, result)

    @mock.patch.object(connections['default'].introspection, 'table_names')
    def test_check_fails(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.side_effect = Exception('Boom')

        response = self.client.get('/database/')

        self.assertEqual(200, response.status_code)

        result = json.loads(response.content.decode())

        expected = {
            u'operational': None,
            u'name': 'DatabaseInformer',
            u'message': 'An error occured when trying access database: Boom'
        }

        self.assertEqual(expected, result)


class MeasureViewTest(TestCase):
    """
    Tests to Measure View
    """

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """
        Test if 'details' from a specific Informer has a expected data
        """
        RawFactory.create(indicator='Database', measure='availability')

        response = self.client.get('/database/availability/')

        self.assertEqual(200, response.status_code)

    @mock.patch.object(Raw.objects, 'filter')
    def test_get_fail(self, m_mock):
        """
        Test if with 'broken scenario', all goes bad
        """
        m_mock.side_effect = Exception('Boom')

        response = self.client.get('/database/availability/')

        self.assertEqual(200, response.status_code)
