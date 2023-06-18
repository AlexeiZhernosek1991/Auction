from django.urls import path
from .views import *

urlpatterns = [path('register/', update_profile, name='register')]
