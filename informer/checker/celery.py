# coding: utf-8

"""django informer checker for Celery"""

from django.conf import settings


from informer.checker.base import BaseInformer, InformerException


from celery.task import task
@task()
def calc(a, b):
    """
    A simple function to help with checking.
    """
    return a + b


class CeleryInformer(BaseInformer):
    """
    Celery Informer.
    """

    def __str__(self):
        return u'Check if Celery is operational.'

    def check(self):
        """
        Perform check against default Celery configuration
        """
        try:
            if 'djcelery' not in settings.INSTALLED_APPS:
                raise InformerException(
                    'djcelery does not appear in the INSTALLED_APPS.')

            result = calc.delay(21, 21)

            if not result.successful():
                return False, 'Celery is out of running.'
        except ImportError:
            raise InformerException(
                'Celery is not installed.')
        except Exception as error:
            raise InformerException(
                'An error occured when trying use Celery: %s.' % error)
        else:
            return True, 'Celery is operational.'
