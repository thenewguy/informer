# coding: utf-8

"""
informer tests for models
"""

import mock
from datetime import datetime

from django.test import TestCase, override_settings
from django.db import models

from freezegun import freeze_time

from informer.models import Raw, generate_raw_data
from informer.checker.base import BaseInformer
from informer.factories import RawFactory


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

    @mock.patch.object(Raw.objects, 'get_or_create')
    @freeze_time('2012-01-14')
    def test_generate_raw_data(self, m_get_or_create):
        generate_raw_data(BaseInformer(), 'foo', 'bar')

        m_get_or_create.assert_called_once_with(
            indicator='Base', value='bar', measure='foo', date=datetime.now())

    @override_settings(DJANGO_INFORMER_PREVENT_SAVE_UNTIL=None)
    @mock.patch.object(Raw.objects, 'get_or_create')
    def test_no_generate_raw_data(self, m_get_or_create):
        """
        If interval was not defined, does not generate the raw data.
        """
        generate_raw_data(BaseInformer(), 'foo', 'bar')

        self.assertFalse(m_get_or_create.called)

    @mock.patch.object(Raw.objects, 'get_or_create')
    def test_no_generate_raw_data_if_limit_not_exceeded(self, m_get_or_create):
        """
        Prevents the generation of multiple data when the limit was not
        exceeded.
        """
        RawFactory(
            indicator='Base', measure='foo', value='bar', date=datetime.now())

        generate_raw_data(BaseInformer(), 'foo', 'bar')

        self.assertFalse(m_get_or_create.called)
