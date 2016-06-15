# coding: utf-8

"""
informer views
"""

import logging
from datetime import datetime, timedelta
from hashlib import sha1

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.cache import patch_response_headers, patch_vary_headers
from django.views.generic import View
from django.conf import settings
from django.contrib.syndication.views import Feed

from informer.checker.base import BaseInformer, InformerException
from informer.models import Raw

logger = logging.getLogger(".".join(["django", __name__]))


class DefaultView(View):
    """
    Default view used for Angular JS web application
    """
    template = 'django-informer-index.html'

    def get(self, request):
        """
        GET /informer/
        """

        interval = getattr(settings, 'DJANGO_INFORMER_PREVENT_SAVE_UNTIL', 0)

        data = {
            'URL': reverse('default-informer'),
            'INTERVAL': interval
        }

        return render(request, self.template, data, content_type='text/html')


class DiscoverView(View):
    """
    Discover URL's from each informer registered on settings
    """

    def get(self, request):
        """
        GET /informer/discover/
        """

        DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

        informers = []

        for namespace, classname in DJANGO_INFORMERS:
            name = classname.replace('Informer', '').lower()
            urlname = 'informer-%s' % name

            informer = {
                'name': name,
                'url': reverse(urlname)
            }

            informers.append(informer)

        return JsonResponse({'result': informers})

class BasicHealthCheckView(View):
    def build_response(self, request, data):
        plain_content_type = "text/plain"
        json_content_type = "application/json"
        raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
        
        json_requested = any([mime.lower().startswith(json_content_type) for mime in raw_content_types])
        
        if json_requested:
            response = JsonResponse(data, status=data["status"])
        else:
            response = HttpResponse(content_type=plain_content_type, **data)
        
        patch_vary_headers(response, ["accept"])
        
        return response
    
    def get(self, request, *args, **kwargs):
        data = dict(content="Status: Online", status=200)
        return self.build_response(request, data)

class HealthCheckView(BasicHealthCheckView):
    informers = getattr(settings, 'DJANGO_INFORMERS', ())

    def get_cache_key(self):
        h = sha1()
        for namespace, classname in self.informers:
            h.update(".".join([namespace, classname]))
        return ";".join([
            "informer",
            self.__class__.__module__,
            self.__class__.__name__,
            h.hexdigest(),
        ])
    
    def build_response(self, request, data):
        cooldown = (data.pop('expires') - datetime.utcnow()).seconds
        response = super(HealthCheckView, self).build_response(request, data)
        patch_response_headers(response, cache_timeout=cooldown)
        return response

    def get(self, request, *args, **kwargs):
        key = self.get_cache_key()
        data = cache.get(key)
        if data is None:
            url = request.build_absolute_uri(reverse('default-informer'))
            caption = ("Status: %s. This is an endpoint for automated monitoring tools. "
                       "Human-readable output available at: {}".format(url))
            data = dict(content=caption % "Healthy", status=200)
            for namespace, classname in self.informers:
                informer = BaseInformer.get_class(namespace, classname)()
                try:
                    operational, message = informer.check_availability()
                except:
                    operational = False
                    message = "Encountered exception during informer health check."
                    logger.exception(message)
                if not operational:
                    data = dict(content=caption % "Unhealthy", status=503)
                    logger.critical("Health checks failed! %s" % message)
                    break
            interval = getattr(settings, 'DJANGO_INFORMER_PREVENT_SAVE_UNTIL', None) or 0
            timeout = 60 * interval
            cooldown = timeout + 1
            data['expires'] = datetime.utcnow() + timedelta(seconds=cooldown)
            cache.set(key, data, timeout)
        return self.build_response(request, data)

class InformerView(View):
    """
    Get results from a specific Informer
    """

    def get(self, request, namespace, classname):
        """
        GET /informer/:name/
        """

        result = {
            'name': classname,
            'operational': None,
            'measures': [],
            'message': 'pending'
        }

        try:
            cls = BaseInformer.get_class(namespace, classname)

            informer = cls()

            measures = cls.get_measures()
            measures = [measure.replace('check_', '') for measure in measures]

            operational, message = informer.check_availability()

            result['operational'] = operational
            result['message'] = message
            result['measures'] = measures
        except InformerException as error:
            result['message'] = '%s' % error

        return JsonResponse(result)


class MeasureView(View):
    """
    Get result from a specific measure
    """

    def get(self, request, namespace, classname, measure):
        """
        GET /informer/:informer/:measure/
        """
        try:
            indicator = classname.replace('Informer', '')
            fields = ['id', 'indicator', 'measure', 'date', 'value']

            data = Raw.objects.filter(
                indicator=indicator, measure=measure).values(*fields)

            result = list(data)
        except Exception as error:
            return JsonResponse({'result': '%s' % error})
        else:
            return JsonResponse({'result': result})


class InformerFeed(Feed):
    title = 'Django Informer'
    link = '/informer/feed/'
    description = 'Latest data collected by Django Informer'

    def items(self):
        return Raw.objects.order_by('-date')[:10]

    def item_title(self, item):  # pragma: no cover
        return '{0} ({1})'.format(item.indicator, item.measure)

    def item_description(self, item):  # pragma: no cover
        return '{0} collected on {1}'.format(item.value, item.date)

    def item_link(self, item):  # pragma: no cover
        return reverse('feed-informer')
