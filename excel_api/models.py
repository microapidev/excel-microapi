from django.db import models


# Create your models here.

class Files(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.FileField(blank=False, null=False, upload_to='files/')

    def __str__(self):
        return self.title
