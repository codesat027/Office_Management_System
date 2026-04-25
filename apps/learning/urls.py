from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('add/', views.add_course, name='add_course'),
    path('<int:id>/', views.course_detail, name='course_detail'),
    path('complete/<int:lesson_id>/', views.mark_complete, name='mark_complete'),
    # path('progress/<int:course_id>/', views.update_progress, name='update_progress'),
]