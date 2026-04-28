from django.contrib import admin
from .models import Attendance, Leave, AdditionalLeave


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('employee__name',)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__name', 'reason')


@admin.register(AdditionalLeave)
class AdditionalLeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'total_days', 'status')
    list_filter = ('status',)
    search_fields = ('employee__name', 'reason')