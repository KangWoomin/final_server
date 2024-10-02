from django.urls import path
from .views import *

app_name = 'streaming'

urlpatterns = [
    path('',view=main, name='main'),

    path('upload_video/', view=upload_video, name='streaming/upload_video'),
]