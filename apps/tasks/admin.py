from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Admin list view mein ye columns dikhenge
    list_display = ('title', 'employee', 'status', 'priority', 'deadline', 'progress')
    
    # Side mein filter aayenge
    list_filter = ('status', 'priority', 'deadline')
    
    # Search bar task title aur employee name ke liye
    search_fields = ('title', 'employee__name')
    
    # Admin se hi progress edit ho sakegi
    list_editable = ('status', 'priority', 'progress')