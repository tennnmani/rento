from django.db import models
from django.urls import reverse
from user.models import User

# Create your models here.
class DateTracker(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_updated = models.DateField()
    def __str__(self):
        return str(self.pk)

class Rent(models.Model):

    status1 = [
        ('paid', 'Paid'),
        ('due', 'Due'),
        ('advance', 'Advance'),
    ]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    room_tag = models.IntegerField(unique=True)
    amount = models.PositiveIntegerField()
    date_paid = models.DateField(null=True)
    amount_paid = models.PositiveIntegerField()
    due = models.PositiveIntegerField()
    advance = models.PositiveIntegerField()
    rent_status = models.CharField(max_length=20, choices=status1)

    def __str__(self):
        return str(self.pk)
