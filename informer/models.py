# coding: utf-8

"""informer models"""

from django.db import connections
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class InformerException(Exception):
    """
    A class to deal with exceptions.
    """
    pass


class BaseInformer(object):
    """
    A base class to serve as infrastructure to new 'Informers'.
    """

    def __str__(self):
        return u'A small and explicit description from informer.'

    def check(self):
        """
        Performs the check.
        """
        raise NotImplementedError

    @staticmethod
    def get_class(namespace, classname):
        """
        Dynamic import from Informer
        """
        try:
            module = __import__(namespace, globals(), locals(), [classname])
            cls = getattr(module, classname)
        except ImportError:
            raise InformerException(
                '%s is unknown or undefined.' % classname)
        except AttributeError:
            raise InformerException(
                'The %s does not exists on %s.' % (classname, namespace))
        except Exception as error:
            raise InformerException(
                'A general exception occurred: %s.' % error)

        if not issubclass(cls, BaseInformer):
            raise InformerException('%s is not a Informer.' % classname)

        return cls


class DatabaseInformer(BaseInformer):
    """
    Database Informer.
    """

    def __str__(self):
        return u'Check if database is operational.'

    def check(self):
        """
        Perform check against default database configuration
        """
        try:
            conn = connections['default']
            conn.introspection.table_names()
        except Exception as error:
            raise InformerException(
                'An error occured when trying access database: %s' % error)
        else:
            return True, 'Your database is operational.'


class StorageInformer(BaseInformer):
    """
    Storage Informer.
    """

    def __str__(self):
        return u'Check if Storage is operational.'

    def check(self):
        """
        Perform check against Default Storage.
        """
        try:
            # TODO: remove if already exists

            # Save data.
            content = ContentFile('File used by StorageInformer checking.')
            path = default_storage.save('./django-informer.txt', content)

            # Check properties.
            default_storage.size(path)
            default_storage.url(path)
            default_storage.path(path)
            default_storage.modified_time(path)
            default_storage.created_time(path)

            # And remove file.
            default_storage.delete(path)

            storage = default_storage.__class__.__name__
        except Exception as error:
            raise InformerException(
                'A error occured when trying access your database: %s' % error)
        else:
            return True, 'Your %s is operational.' % storage
