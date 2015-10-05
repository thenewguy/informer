# coding: utf-8

"""informer models"""

from datetime import datetime

from django.db import models

class Raw(models.Model):
    """
    Raw data collected by informer checker.
    """

    indicator = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (('indicator', 'measure', 'date'),)
        index_together = [['indicator', 'measure', 'date'],]
        ordering = ['-date', 'indicator', 'measure']

    def __str__(self):
        return u'%s' % self.name
