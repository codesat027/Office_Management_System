"""
URL configuration for oms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import login_view

urlpatterns = [
    path('', login_view, name='home'),

    path('accounts/', include('apps.accounts.urls')),
    path('employees/', include('apps.employees.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('learning/', include('apps.learning.urls')),
    path('notices/', include('apps.notices.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('birthday-anniversary/', include('apps.birthday_anniversary.urls')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)