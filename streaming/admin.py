from django.contrib import admin
from .models import *

# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ['path','upload_at']
    list_display_links =['path']

admin.site.register(Videos, VideoAdmin)