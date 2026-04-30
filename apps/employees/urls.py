from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('profile/', views.profile_view, name='profile_view'),
    
    # Document related URLs (Important!)
    path('upload-document/', views.upload_document, name='upload_document'),
    path('delete-document/<int:id>/', views.delete_document, name='delete_document'),
    path('view-document/<int:id>/', views.view_document, name='view_document'),
]