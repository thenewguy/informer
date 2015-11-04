# coding: utf-8

"""
django informer checker base
"""

from importlib import import_module

from informer.models import post_check


class InformerException(Exception):
    """
    A class to deal with exceptions.
    """
    pass


class BaseInformer(object):
    """
    A (base) class to serve as infrastructure to new 'Informers'.
    """

    def __str__(self):
        return u'A small and explicit description from informer.'

    def __new__(cls, *args, **kwargs):
        """
        On instantiation, the trigger is added.
        """
        measures = cls.get_measures()

        for measure in measures:
            func = getattr(cls, measure)
            setattr(cls, measure, trigger(func))

        return super(BaseInformer, cls).__new__(cls)

    def check_availability(self):
        """
        Each informer need check the availability from resource or service.
        """
        raise NotImplementedError

    @staticmethod
    def get_class(namespace, classname):
        """
        Dynamic import from Informer
        """
        try:
            module = import_module(namespace)
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

    @classmethod
    def get_measures(cls):
        """
        Get measures
        """
        measures = []

        for attr in dir(cls):
            if not attr.startswith('check_'):
                continue

            if attr not in measures:
                measures.append(attr)

        return measures


def trigger(func):
    def save(cls, *args, **kwargs):
        sender = cls
        measure = func.__name__
        value = func(cls)

        post_check.send(sender=sender, measure=measure, value=value[0])

        return value

    return save
