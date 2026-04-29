from django.db import models
from django.contrib.auth.models import User
from apps.employees.models import Employee

class Task(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Urgent', 'Urgent')]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks') # Kisko diya
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Kisne diya
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    deadline = models.DateField(blank=True, null=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.title