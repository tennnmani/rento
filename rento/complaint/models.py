from django.db import models
from django.urls import reverse
from rooms.models import Room


report_detail = [
    ('fake_contact', 'Fake Contact'),
    ('fake_room', 'Fake Room'),
    ('misleading', 'Misleading Description'),
    ('other', 'Other'),
]
# Create your models here.


class report(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    report_type = models.CharField(
        max_length=20, choices=report_detail, default='fake_contact')
    report_description = models.TextField(default='Descripe complaint')
    
    
    def __str__(self):
        return self.report_type
