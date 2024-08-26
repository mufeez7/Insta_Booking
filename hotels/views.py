from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Hotel, Room,Booking
from .forms import SignUpForm, BookingFilterForm, BookingConfirmationForm, SearchForm
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.views.generic import ListView
from django.core.paginator import Paginator

import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

import requests
from django.http import JsonResponse



def homepage_view(request):
    return render(request, 'homepage.html')

def hotel_list_view(request):
    hotels = Hotel.objects.all()
    paginator = Paginator(hotels, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    hotel_count = hotels.count()
    return render(request, 'hotels/hotel_list.html', {'page_obj': page_obj, 'hotel_count': hotel_count})

def hotel_detail_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})


def signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = SignUpForm()

    return render(request,'hotels/signup.html', {'form':form})

def show_bookings(request):
    locations = Hotel.objects.values_list('location', flat=True).distinct()
    room_count = 0

    if request.method == "POST":
        form = BookingFilterForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            min_rating = form.cleaned_data['min_rating']

            available_rooms = Room.objects.filter(hotel__location=location, availability=True)
            if min_price:
                available_rooms = available_rooms.filter(price_per_night__gte=min_price)
            if max_price:
                available_rooms = available_rooms.filter(price_per_night__lte=max_price)
            if min_rating:
                available_rooms = available_rooms.filter(hotel__rating__gte=min_rating)

            if check_in_date < timezone.now().date() or check_out_date < check_in_date:
                raise ValidationError("Invalid dates. Please select future dates.")
            

            final_available_rooms = []
            for room in available_rooms:
                if room.is_available(check_in_date, check_out_date):
                    final_available_rooms.append(room)
            
            #for different time periods
            conflict_rooms = Room.objects.filter(hotel__location=location, availability=False)
            for room in conflict_rooms:
                bookings = Booking.objects.filter(room=room)
                temp_avail = True

                for booking in bookings:
                    if not (check_out_date <= booking.check_in or check_in_date >= booking.check_out):
                        temp_avail = False
                        break
                    if temp_avail:
                        room.availability = True
                        room.save()
                        final_available_rooms.append(room)

            paginator = Paginator(final_available_rooms, 10) 
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            room_count = len(final_available_rooms)
            return render(request, 'hotels/show_bookings_results.html', {'page_obj': page_obj, 'room_count': room_count, 
                                                                         'location': location})
    else:
        form = BookingFilterForm()
    return render(request, 'hotels/show_bookings.html', {'form': form, 'locations': locations})

def reserve_confirmation(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    check_in_date = request.GET.get('check_in')
    check_out_date = request.GET.get('check_out')
    print("Check in: ", check_in_date)
    print("Check out: ",check_out_date)

    if request.method == "POST":
        form = BookingConfirmationForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
        
            Booking.objects.create(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out
            )
            room.availability = False
            room.save()
            return redirect('homepage')  

    else:
        form = BookingConfirmationForm(initial={
            'check_in': check_in_date,
            'check_out': check_out_date
        })

    return render(request, 'hotels/reserve_confirmation.html', {'form': form, 'room': room})
    
def my_bookings(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    bookings = Booking.objects.filter(user=request.user)
    paginator = Paginator(bookings, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    booking_count = bookings.count()
    return render(request, 'hotels/my_bookings.html', {"page_obj": page_obj, "booking_count": booking_count})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == "POST":

        booking.delete()
        return redirect('my_bookings') 
    
    return redirect('my_bookings')


#model loading
rfc = joblib.load('models/rfc_model.pkl')
le_hotel_name = joblib.load('models/le_hotel_name.pkl')  
le_room_type = joblib.load('models/le_room_type.pkl')
le_location = joblib.load('models/le_location.pkl')

def predict_recommendation(location, room_type, price_per_night, rating):
    location_encoded = le_location.transform([location])[0]
    room_encoded = le_room_type.transform([room_type])[0]

    features = np.array([[location_encoded, rating, room_encoded, price_per_night]])
    hotel_encoded = rfc.predict(features)[0]

    recommended_hotel = le_hotel_name.inverse_transform([hotel_encoded])[0]
    return recommended_hotel

def recommend_room(request):
    recommendation = None
    hotel_details = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            room_type = form.cleaned_data['room_type']
            price_per_night = form.cleaned_data['price_per_night']
            rating = form.cleaned_data['rating']
            recommendation = predict_recommendation(location, room_type, price_per_night, rating)
            print(recommendation)
            hotel_details = get_object_or_404(Hotel, name=recommendation)

    else:
        form = SearchForm()
    
    return render(request, 'hotels/recommendation.html', {'form': form, 'hotel_details': hotel_details})

def index(request):
    user_id = request.user.id if request.user.is_authenticated else None
    
    return render(request, "hotels/chatbot.html", {
        'user': request.user,
        'user_id': user_id
    })