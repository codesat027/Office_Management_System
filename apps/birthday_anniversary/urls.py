from django.urls import path
from . import views

urlpatterns = [
    path('', views.birthday_list, name='birthday_list'),
]