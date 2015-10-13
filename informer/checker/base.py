# coding: utf-8

"""
django informer checker base
"""

import types

from informer.models import Raw


class InformerException(Exception):
    """
    A class to deal with exceptions.
    """
    pass


class RawManager(type):

    prefix = 'check_'

    @staticmethod
    def save(func):
        def helper(instance, *args, **kwargs):
            result = func(instance, *args, **kwargs)

            Raw.objects.get_or_create(
                indicator=instance.__class__.__name__,
                measure=func.func_name.replace('check_', ''),
                value=result[0])

            return result

        return helper

    @staticmethod
    def trigger(func):
        """
        Trigger added to 'check' method, to run all checks specified by prefix.
        """
        def helper(instance, *args, **kwargs):
            result = func(instance, *args, **kwargs)

            collectors = [c for c in dir(instance)\
                if c.startswith(RawManager.prefix)]

            for collector in collectors:
                getattr(instance, collector, None)()

            return result

        return helper

    def __new__(cls, clsname, superclasses, attributedict):
        """
        On instantiation, the triggers are added.
        """

        for item in attributedict:
            attr = attributedict[item]

            if not callable(attr):
                continue

            if not isinstance(attr, types.FunctionType):
                continue

            if not attr.func_name.startswith('check_'):
                continue

            name = attr.func_name

            # bind method that start with 'check_'.
            attributedict[name] = cls.save(attributedict[name])

        # bind method 'check' to trigger all checks.
        attributedict['check'] = cls.trigger(attributedict['check'])

        return type.__new__(cls, clsname, superclasses, attributedict)


class BaseInformer(object):
    """
    A base class to serve as infrastructure to new 'Informers'.
    """

    __metaclass__ = RawManager

    def __str__(self):
        return u'A small and explicit description from informer.'

    def check(self):
        """
        Each informer need 'inspect' the guarded resource or service.
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
