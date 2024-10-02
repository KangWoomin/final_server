from django.db import models


# Create your models here.

class Videos(models.Model):
    path = models.CharField(verbose_name='경로', max_length=100)
    upload_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    file = models.FileField(verbose_name='비디오파일', upload_to='video/')

    def __str__(self):
        return self.path
