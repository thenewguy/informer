# coding: utf-8

"""informer models"""

from django.db import connections


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
    Database informer.
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
                'a error occured when trying access your database: %s' % error)
        else:
            return True, 'Your database is operational'
