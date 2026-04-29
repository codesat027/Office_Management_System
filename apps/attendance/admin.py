from django.contrib import admin
from .models import Attendance, Leave, AdditionalLeave

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('employee__name',)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    # 'total_days' property hai, isliye ise list_display mein dikha sakte hain
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__name', 'reason')
    # Bulk delete action hamesha enable rehta hai

@admin.register(AdditionalLeave)
class AdditionalLeaveAdmin(admin.ModelAdmin):
    # Yahan list_display ko update kar diya hai
    list_display = ('employee', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('employee__name', 'reason')
    
    # Isse aapko admin panel mein list ke upar "Delete selected additional leaves" ka option milega
    actions = ['delete_selected']