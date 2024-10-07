from django.db import models

# Create your models here.

class FilePath(models.Model):
    path = models.CharField(verbose_name='경로', max_length=255)
    update_dt = models.DateTimeField(verbose_name='업데이트 시간', auto_now=True)
    