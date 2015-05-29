# coding: utf-8

"""informer tests for views"""

import mock
import json
import pytest

from django.test import TestCase, Client
from django.db import connections

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


class InformerDiscoverViewTest(TestCase):
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
            'informers': [{
                'url': '/database/',
                'name': 'database'
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
            'message': 'Your database is operational',
            'name': 'DatabaseInformer',
            'operational': True
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
            'operational': None,
            'name': 'DatabaseInformer',
            'message': 'a error occured when trying access your database: Boom'
        }

        self.assertEqual(expected, result)
