from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    amenities = models.TextField()
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def is_available(self, check_in, check_out):
        overlapping_bookings = self.booking_set.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        return not overlapping_bookings.exists()
    
    def __str__(self):
        return f'{self.room_type} - {self.hotel.name}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.room.hotel.name} ({self.check_in} to {self.check_out})'