import os
from django.db import models

# Create your models here.
class Document(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')

    @property
    def filename(self):
        return os.path.basename(self.uploaded_file.name)