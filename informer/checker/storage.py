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
    storage = default_storage
    filename = 'django-informer.txt'

    def __str__(self):
        return u'Check if %s is operational.' % self.storage.__class__.__name__

    def check_availability(self):
        """
        Perform check against Storage.
        """
        filename = self.storage.get_valid_name(self.filename)

        try:
            if self.storage.exists(filename):
                try:
                    self.storage.delete(filename)
                except NotImplementedError:
                    pass

            # Save data.
            content = ContentFile('File used by StorageInformer checking.')
            path = self.storage.save(filename, content)

            # Check properties.
            try:
                self.storage.size(path)
            except NotImplementedError:
                pass

            try:
                self.storage.url(path)
            except NotImplementedError:
                pass

            try:
                self.storage.path(path)
            except NotImplementedError:
                pass

            try:
                self.storage.modified_time(path)
            except NotImplementedError:
                pass

            try:
                self.storage.created_time(path)
            except NotImplementedError:
                pass

            # And remove file.
            try:
                self.storage.delete(path)
            except NotImplementedError:
                pass

        except Exception as error:
            raise InformerException(
                'A error occured when trying access your database: %s' % error)
        else:
            return (True,
                    'Your %s is operational.' % self.storage.__class__.__name__)
