# coding: utf-8

"""
informer tests for models
"""

from django.test import TestCase
from django.db import models

from informer.models import Raw


class RawTestCase(TestCase):
    def test_sanity(self):
        meta = Raw._meta

        indicator = meta.get_field('indicator')
        measure = meta.get_field('measure')
        date = meta.get_field('date')
        value = meta.get_field('value')

        self.assertTrue(issubclass(Raw, models.Model))

        self.assertIsInstance(indicator, models.CharField)
        self.assertIsInstance(measure, models.CharField)
        self.assertIsInstance(date, models.DateTimeField)
        self.assertIsInstance(value, models.CharField)

    def test_unicode(self):
        expected = 'Bar (Foo)'

        raw = Raw(indicator='Foo', measure='Bar', value=True)

        self.assertEqual(expected, str(raw))
