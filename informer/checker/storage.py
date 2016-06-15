# coding: utf-8

"""
django informer checker for Storage
"""
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from informer.checker.base import BaseInformer, InformerException
from __builtin__ import False


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
                    verify_filename = False
                else:
                    verify_filename = True

            # Save data.
            data = uuid4().hex
            content = ContentFile(data)
            path = self.storage.save(filename, content)

            # Check saved file name
            if verify_filename:
                if path != filename:
                    raise InformerException(
                    ('Invalid filename returned after writing to your '
                     '%s storage.') %
                    self.storage.__class__.__name__)

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
            
            # Check written data matches read data
            if self.storage.open(path).read() != data:
                raise InformerException(
                'Invalid data read after writing to your %s storage.' %
                self.storage.__class__.__name__)

            # And remove file.
            try:
                self.storage.delete(path)
            except NotImplementedError:
                pass

        except Exception as error:
            raise InformerException(
                'A error occured when trying access your %s storage: %s' % (
                self.storage.__class__.__name__, error))
        else:
            return (True,
                    'Your %s is operational.' % self.storage.__class__.__name__)
