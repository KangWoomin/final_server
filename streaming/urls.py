from django.urls import path
from .views import *

app_name = 'streaming'

urlpatterns = [
    path('',view=main, name='main'),
]