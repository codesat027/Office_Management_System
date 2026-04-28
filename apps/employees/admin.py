from django.contrib import admin
from .models import Employee, Document


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'position', 'leave_balance')
    search_fields = ('name', 'email', 'department', 'position')
    list_filter = ('department', 'position')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'uploaded_at')
    search_fields = ('title', 'employee__name')