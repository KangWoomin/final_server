from django.urls import path
from .views import *

app_name = 'streaming'

urlpatterns = [
    path('',view=main, name='main'),

    path('stream_video/<str:filename>', view=stream_video, name='stream_video'),
    path('upload_video/', view=upload_video, name='upload_video'),

  
]