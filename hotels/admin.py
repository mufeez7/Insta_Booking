from django.contrib import admin

# Register your models here.
from .models import Hotel, Room, Booking


class HotelAdmin(admin.ModelAdmin):
    # Add the search functionality
    search_fields = ['name']

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room)
admin.site.register(Booking)