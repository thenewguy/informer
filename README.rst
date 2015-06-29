Django Informer
==============

.. image:: https://img.shields.io/pypi/v/django-informer.svg
   :alt: PyPi page
   :target: https://pypi.python.org/pypi/django-informer

.. image:: https://img.shields.io/pypi/l/django-informer.svg
   :alt: License MIT
   :target: https://github.com/rodrigobraga/informer/blob/master/LICENSE

A pluggable app to monitoring your own infrastructure and third party services.

Quick Start
-----------------

Below a quick guide to install and run, more detailed documentation is in the `docs <docs>`_ directory.

Install Django Informer
-----------------

::

    pip install django_informer


Add "informer" to your INSTALLED_APPS
-----------------

::

    INSTALLED_APPS = (
      ...
      'informer',
    )


Set informers on settings
-----------------
  
::

    DJANGO_INFORMERS = (
        ('informer.checker.database', 'DatabaseInformer'),
        ('informer.checker.storage', 'StorageInformer'),
        ('informer.checker.celery', 'CeleryInformer'),
    )


Include the URLconf in your project urls.py
-----------------

::

    url(r'^informer/', include('informer.urls')),


Run migrate to create the informer models
-----------------

::

    python manage.py migrate

Run
-----------------

Start the development server and visit http://127.0.0.1:8000/informer/ to view monitoring results.

.. _doc: https://github.com/rodrigobraga/informer/tree/master/docs
