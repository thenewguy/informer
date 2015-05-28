# Django Informer

[![wercker status](https://app.wercker.com/status/0d5743ef22b8fe14d2929ec4d987ef0d/s "wercker status")](https://app.wercker.com/project/bykey/0d5743ef22b8fe14d2929ec4d987ef0d)

A pluggable app to monitoring your own infrastructure and third party services.

Detailed documentation is in the "docs" directory.

## Quick start

1. Add "informer" to your INSTALLED_APPS setting like this::

```
    INSTALLED_APPS = (
        ...
        'informer',
    )
```

2. Include a list from informers on settings

```
DJANGO_INFORMERS = (
    ('informer.models', 'DatabaseInformer'),
)
```

3. Include the URLconf in your project urls.py like this::

```
    url(r'^informer/', include('informer.urls')),
```

4. Run ```python manage.py migrate``` to create the informer models.

5. Start the development server and visit http://127.0.0.1:8000/informer/ to view monitoring results.
