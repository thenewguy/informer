# coding: utf-8

"""informer views"""

from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from django.conf import settings

from informer.models import BaseInformer, InformerException


class DefaultView(View):
    """
    Default view used for Angular JS web application
    """
    template = 'django-informer-index.html'

    def get(self, request):
        """
        GET /informer/
        """

        data = {
            'URL': reverse('default-informer')
        }

        return render(request, self.template, data, content_type='text/html')


class InformerDiscoverView(View):
    """
    Discover URL's from each informer registered on settings
    """

    def get(self, request):
        """
        GET /informer/discover/
        """

        informers = []

        for namespace, classname in settings.DJANGO_INFORMERS:
            name = classname.replace('Informer', '').lower()
            urlname = 'informer-%s' % name

            informer = {
                'name': name,
                'url': reverse(urlname)
            }

            informers.append(informer)

        return JsonResponse({'informers': informers})


class InformerView(View):
    """
    Get result from a specific Informer
    """

    def get(self, request, namespace, classname):
        """
        GET /informer/:name/
        """
        cls = BaseInformer.get_class(namespace, classname)

        informer = cls()

        result = {
            'name': classname,
            'operational': None,
            'message': 'pending'
        }

        try:
            operational, message = informer.check()

            result['operational'] = operational
            result['message'] = message
        except InformerException as error:
            result['operational'] = False
            result['message'] = '%s' % error

        return JsonResponse(result)
