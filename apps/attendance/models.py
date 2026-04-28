from django.db import models
from apps.employees.models import Employee


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"


class Leave(models.Model):
    LEAVE_TYPES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Paid Leave', 'Paid Leave'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPES, default='Sick Leave')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type}"


class AdditionalLeave(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee.name} - Additional Leave"