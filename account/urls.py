from django.urls import path
from .views import *

urlpatterns = [
    path('', view=main, name='main'),
    path('create_user/', view=create_user, name='create_user'),
    path('user_login/', view=user_login, name='user_login'),
    path('user_logout/', view=user_logout, name='user_logout'),
]