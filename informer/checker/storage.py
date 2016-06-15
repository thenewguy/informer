# coding: utf-8

"""
django informer checker for Storage
"""

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from informer.checker.base import BaseInformer, InformerException


class StorageInformer(BaseInformer):
    """
    Storage Informer.
    """

    def __str__(self):
        return u'Check if Storage is operational.'

    def check_availability(self):
        """
        Perform check against Default Storage.
        """
        try:
            # TODO: remove if already exists

            # Save data.
            content = ContentFile('File used by StorageInformer checking.')
            path = default_storage.save('./django-informer.txt', content)

            # Check properties.
            try:
                default_storage.size(path)
            except NotImplementedError:
                pass

            try:
                default_storage.url(path)
            except NotImplementedError:
                pass

            try:
                default_storage.path(path)
            except NotImplementedError:
                pass

            try:
                default_storage.modified_time(path)
            except NotImplementedError:
                pass

            try:
                default_storage.created_time(path)
            except NotImplementedError:
                pass

            # And remove file.
            try:
                default_storage.delete(path)
            except NotImplementedError:
                pass

            storage = default_storage.__class__.__name__
        except Exception as error:
            raise InformerException(
                'A error occured when trying access your database: %s' % error)
        else:
            return True, 'Your %s is operational.' % storage
