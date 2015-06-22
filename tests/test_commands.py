# coding: utf-8

"""informer tests for commands"""

import mock
import pytest

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from django.db import connections
from django.conf import settings

from informer.checker.base import BaseInformer, InformerException
from informer.checker.database import DatabaseInformer
from informer.checker.storage import StorageInformer
from informer.checker.celery import CeleryInformer


pytestmark = pytest.mark.django_db


class InformerTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('checkinformers', stdout=out)

        expected = """Checking Informers.
-------------------------------------------------------------------------------

\tDatabaseInformer
\t\toperational: True
\t\tmessage: Your database is operational.

\tStorageInformer
\t\toperational: True\n\t\tmessage: Your FileSystemStorage is operational.
"""

        self.assertEqual(expected, out.getvalue())

    @mock.patch('informer.checker.base.BaseInformer.get_class')
    def test_command_failure(self, m_mock):
        m_mock.side_effect = CommandError('Cataploft')

        self.assertRaises(CommandError, call_command, 'checkinformers')
