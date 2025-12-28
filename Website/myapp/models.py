from django.db import models

# Create your models here.
class UploadFile(models.Model):
    file = models.FileField(upload_to='media/')
    uploaded_at =  models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name