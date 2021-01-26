from django.db import models
from django.urls import reverse
from rooms.models import Room
from user.models import User

# Create your models here.
class Enquiry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null= True, blank= True, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    phone = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=300,)
    occupation = models.CharField(max_length=200)
    question = models.TextField(default='If any confusion ask here..')
    


    def __str__(self):
        return self.name