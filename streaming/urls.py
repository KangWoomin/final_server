from django.urls import path
from .views import *
from . import consumers

app_name = 'streaming'

urlpatterns = [
    path('',view=main, name='main'),

    
    path('upload_video/', view=upload_video, name='upload_video'),

    path("upload/", view=upload ,name='upload'),
  
]

websocket_urlpatterns = [
    path('ws/stream/', consumers.StreamConsumer.as_asgi()),
]