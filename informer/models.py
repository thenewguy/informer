# coding: utf-8

"""
informer models
"""

from django.db import models
from django.dispatch import Signal


class Raw(models.Model):
    """"
    Raw data collected by informer.
    """

    indicator = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (('indicator', 'measure', 'date'),)
        index_together = [['indicator', 'measure', 'date'], ]
        ordering = ['-date', 'indicator', 'measure']

    def __str__(self):
        return u'%s (%s)' % (self.measure, self.indicator)


post_check = Signal(providing_args=['measure', 'value'])


def generate_raw_data(sender, measure, value, *args, **kwargs):
    """
    Generate raw data from Informer.
    """
    indicator = sender.__class__.__name__.replace('Informer', '')
    measure = measure.replace('check_', '')

    Raw.objects.get_or_create(
        indicator=indicator, measure=measure, value=value)

post_check.connect(generate_raw_data, sender=None)
