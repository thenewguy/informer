# coding: utf-8

"""
informer URL configuration
"""

from django.conf import settings
from django.conf.urls import url

from informer.checker.base import BaseInformer

from informer.views import (
    BasicHealthCheckView, DefaultView, DiscoverView, HealthCheckView,
    InformerView, MeasureView, InformerFeed)


urlpatterns = [
    url(r'^$', DefaultView.as_view(), name='default-informer'),
    url(r'^discover/$', DiscoverView.as_view(), name='discover-informer'),
    url(r'^feed/$', InformerFeed(), name='feed-informer'),
    url(r'^health/$', HealthCheckView.as_view(), name='informer-health'),
    url(r'^ping/$', BasicHealthCheckView.as_view(), name='informer-ping'),
]

DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

for namespace, classname in DJANGO_INFORMERS:
    data = {'namespace': namespace, 'classname': classname}
    informer = classname.replace('Informer', '').lower()
    alias = 'informer-%s' % informer

    uri = url(r'^%s/$' % informer, InformerView.as_view(), data, name=alias)

    urlpatterns.append(uri)

    # append url from measures
    cls = BaseInformer.get_class(namespace, classname)
    view = MeasureView.as_view()

    for measure in cls.get_measures():
        measure = measure.replace('check_', '')
        alias = 'informer-%s-%s' % (informer, measure)

        data = {
            'namespace': namespace,
            'classname': classname,
            'measure': measure
        }

        uri = url(r'^%s/%s/$' % (informer, measure), view, data, name=alias)

        urlpatterns.append(uri)
    
    # add healthcheck url
    alias = 'informer-health-%s' % informer
    uri = url(r'^health/%s/$' % informer, HealthCheckView.as_view(informers=[(namespace, classname)]), name=alias),
