from django.db import models
from django.urls import reverse
from user.models import User

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=120) # max_length = required

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.CharField(max_length=120) # max_length = required
    code = models.CharField(max_length=500) # max_length = required

    def __str__(self):
        return self.location
    
    @staticmethod
    def get_all_locations():
        return Location.objects.all()

class Room(models.Model):
    
    status1 = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]
    status2 = [
        ('not_featured', 'Not Featured'),
        ('featured', 'Featured'),
        ('feature_request', 'Featured Request'),
        ('denied', 'Featured Denied'),
    ]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    house_number = models.CharField(max_length=120) # max_length = required
    description = models.TextField(blank=True, null=True)
    floor       = models.PositiveSmallIntegerField()
    price       = models.PositiveSmallIntegerField()
    #images
    image1 = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    image3 = models.ImageField(upload_to='')
    #facility
    water = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    parking = models.PositiveSmallIntegerField(default=0)
    c_parking = models.PositiveSmallIntegerField(default=0)
    #rooms
    bedroom = models.PositiveSmallIntegerField(default=1)
    bathroom = models.PositiveSmallIntegerField(default=1)

    description     = models.TextField(max_length=500,blank=False, null=False)
    date_posted = models.DateField(auto_now_add=True)
    views = models.PositiveSmallIntegerField(default=0)
    blocked = models.BooleanField(default=False)
    room_status = models.CharField(max_length=20, choices=status1, default='public')
    total_enquiry = models.PositiveSmallIntegerField(default=0)
    total_report = models.PositiveSmallIntegerField(default=0)
    featured = models.CharField(max_length=100, choices=status2, default='not_featured')
    featured_date = models.DateField(null=True,blank=True)
    feature_end = models.DateField(null=True,blank=True)
    times_featured = models.PositiveSmallIntegerField(default=0)
    day_remaning = models.PositiveSmallIntegerField(default=0)
    declined_date = models.DateField(null=True,blank=True)
    
    

        

    def __str__(self):
        return str(self.pk)

    @staticmethod
    def get_all_rooms():
        return Room.objects.all()

    @staticmethod
    def get_all_rooms_by_filter(location_id):
        if location_id:
            return Room.objects.filter(location = location_id)
        else:
            return Room.get_all_rooms()

    @staticmethod
    def get_all_rooms_by_waterinternetparkingfilter(water_id,internet_id,parking_id):
            return Room.objects.filter(water = water_id, internet = internet_id, parking = parking_id)
    
    @staticmethod
    def get_all_rooms_by_allfilter(location_id,water_id,internet_id,parking_id):
            return Room.objects.filter(location = location_id,water = water_id, internet = internet_id, parking = parking_id)

    # def get_absolute_url(self):
    #     return reverse("products:product-detail", kwargs={"id": self.id}) #f"/products/{self.id}/"