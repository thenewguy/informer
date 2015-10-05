# coding: utf-8

"""
informer signals
"""

from django.dispatch import Signal

post_check = Signal(providing_args=['metric', 'value'])
