from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('add/', views.add_attendance, name='add_attendance'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/add/', views.add_leave, name='add_leave'),
    path('leave/approve/<int:id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:id>/', views.reject_leave, name='reject_leave'),
    path('leave/report/', views.leave_report, name='leave_report'),
    path('leave/balance/', views.leave_balance, name='leave_balance'),
    path('leave/additional/', views.add_additional_leave, name='add_additional_leave'),
]