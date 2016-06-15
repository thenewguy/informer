# coding: utf-8

"""
django informer checker for Storage
"""
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.encoding import force_text

from informer.checker.base import BaseInformer, InformerException


class StorageInformer(BaseInformer):
    """
    Storage Informer.
    """
    storage = default_storage
    filename = 'django-informer.txt'

    @property
    def storage_name(self):
        return self.storage.__class__.__name__

    def __str__(self):
        return u'Check if %s is operational.' % self.storage_name

    def check_availability(self):
        """
        Perform check against Storage.
        """
        valid_filename = self.storage.get_valid_name(self.filename)

        try:
            verify_filename = False
            if self.storage.exists(valid_filename):
                try:
                    self.storage.delete(valid_filename)
                except NotImplementedError:
                    pass
                else:
                    verify_filename = True

            # Save data.
            data = force_text(uuid4().hex)
            content = ContentFile(data)
            saved_filename = self.storage.save(valid_filename, content)

            # Check saved file name
            if verify_filename:
                if saved_filename != valid_filename:
                    raise InformerException(
                        ('Incorrect filename returned after writing to your '
                         '%s storage.') % self.storage_name)

            # Check methods.
            try:
                if content.size != self.storage.size(saved_filename):
                    raise InformerException(
                        'Incorrect size reported by your %s storage.' %
                        self.storage_name)
            except NotImplementedError:
                pass

            try:
                self.storage.url(saved_filename)
            except NotImplementedError:
                pass

            try:
                self.storage.path(saved_filename)
            except NotImplementedError:
                pass

            try:
                self.storage.modified_time(saved_filename)
            except NotImplementedError:
                pass

            try:
                self.storage.created_time(saved_filename)
            except NotImplementedError:
                pass

            # Check written data matches read data
            if self.storage.open(saved_filename).read() != data:
                raise InformerException(
                    'Invalid data read after writing to your %s storage.' %
                    self.storage_name)

            # And remove file.
            try:
                self.storage.delete(saved_filename)
            except NotImplementedError:
                pass

        except Exception as error:
            raise InformerException(
                'A error occured when trying access your %s storage: %s' % (
                    self.storage_name, error))
        else:
            return (True, 'Your %s is operational.' % self.storage_name)
