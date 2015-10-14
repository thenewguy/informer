# coding: utf-8

"""
django informer checker base
"""

from informer.models import post_check


class InformerException(Exception):
    """
    A class to deal with exceptions.
    """
    pass


class Collector(type):
    """
    A helper to automate the bind of the collector of measurements.
    """

    @staticmethod
    def trigger(func):
        """
        Trigger fired after checking by the signal.
        """
        def helper(instance, *args, **kwargs):
            result = func(instance, *args, **kwargs)

            # save default (availability)
            post_check.send(
                sender=instance, measure='availability', value=result[0])

            # run others checks
            attrs = dir(instance)
            collectors = [attr for attr in attrs if attr.startswith('check_')]

            for collector in collectors:
                value = getattr(instance, collector, None)()
                post_check.send(
                    sender=instance, measure=collector, value=value)

            return result

        return helper

    def __new__(cls, clsname, superclasses, attributedict):
        """
        On instantiation, the trigger is added.
        """
        attributedict['check'] = cls.trigger(attributedict['check'])

        return type.__new__(cls, clsname, superclasses, attributedict)


class BaseInformer(object):
    """
    A base class to serve as infrastructure to new 'Informers'.
    """

    __metaclass__ = Collector

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
