from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    leave_balance = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title