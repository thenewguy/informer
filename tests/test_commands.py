# coding: utf-8

"""informer tests for commands"""

import mock
import pytest

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils.six import StringIO

pytestmark = pytest.mark.django_db


class InformerTest(TestCase):
    def test_command_list(self):
        out = StringIO()
        call_command('checkinformer', '--list', stdout=out)

        expected = [
            'Below the informers that appear in settings.',
            'informer.checker.database.DatabaseInformer',
            'informer.checker.storage.StorageInformer',
            'informer.checker.celery.CeleryInformer']

        result = out.getvalue()

        for item in expected:
            self.assertTrue(item in result)

    def test_command_check_with_all(self):
        """
        Call command without specify a Informer.
        """
        out = StringIO()
        call_command('checkinformer', stdout=out)

        expected = [
            'Checking Informers.',
            'Checking StorageInformer... Your FileSystemStorage is '
            'operational.']

        result = out.getvalue()

        for item in expected:
            self.assertTrue(item in result)

    def test_command_check_with_one(self):
        """
        Call command specifying an informer.
        """
        out = StringIO()
        call_command('checkinformer', 'DatabaseInformer', stdout=out)

        expected = [
            'Checking Informers.',
            'Checking DatabaseInformer... Your database is operational.']

        result = out.getvalue()

        for item in expected:
            self.assertTrue(item in result)

    def test_command_check_with_unknown_informer(self):
        """
        Call command specifying an unknown informer are (silently) ignored.
        """
        out = StringIO()
        call_command('checkinformer', 'UnknownInformer', stdout=out)

        expected = [
            'No informer was found with names provided (UnknownInformer).']

        result = out.getvalue()

        for item in expected:
            self.assertTrue(item in result)

    def test_command_without_configuration(self):
        """
        Show a friendly message when missing configuration.
        """
        with override_settings(DJANGO_INFORMERS=None):
            out = StringIO()
            call_command('checkinformer', stdout=out)

            expected = [
                'No informer was found.',
                'Missing configuration.']

            result = out.getvalue()

            for item in expected:
                self.assertTrue(item in result)

    @mock.patch('informer.checker.base.BaseInformer.get_class')
    def test_command_failure(self, m_mock):
        m_mock.side_effect = Exception('Cataploft')

        out = StringIO()

        call_command('checkinformer', stderr=out)

        expected = ['A generic exception occurred: Cataploft']

        result = out.getvalue()

        for item in expected:
            self.assertTrue(item in result)
