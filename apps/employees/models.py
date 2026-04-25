from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name