from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ]
    status = [
    ('blocked', 'Blocked'),
    ('clear', 'Clear'),
    ]

    location = models.CharField(max_length=120)
    gender = models.CharField(
        choices=GENDER_CHOICES, 
        max_length= 120, 
        null= True,
        blank= True
    )
    phone_number = models.IntegerField(null=True,unique=True)
    user_status = models.CharField(
        max_length=20, choices=status, default='clear')
    email = models.EmailField(unique=True)
    total_rooms = models.IntegerField(default=0)
    total_reports = models.IntegerField(default=0)
    total_enquiry = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
