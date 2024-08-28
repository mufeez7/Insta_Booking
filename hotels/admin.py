from django.contrib import admin

# Register your models here.
from .models import Hotel, Room, Booking


class HotelAdmin(admin.ModelAdmin):
    search_fields = ['name']

class RoomAdmin(admin.ModelAdmin):
    search_fields = ['hotel__name']

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking)