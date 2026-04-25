from django.db import models
from apps.employees.models import Employee
from datetime import date


class BirthdayAnniversary(models.Model):
    EVENT_CHOICES = [
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    event_date = models.DateField()
    years_completed = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        today = date.today()

        if self.event_type == 'Anniversary':
            self.years_completed = today.year - self.event_date.year
        else:
            self.years_completed = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.event_type}"