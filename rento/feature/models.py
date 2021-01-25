from django.db import models

# Create your models here.
class counter(models.Model):
    counter = models.IntegerField(default=0)