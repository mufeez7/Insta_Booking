from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hotel, Room
from django.utils.dateparse import parse_date
from django.forms import DateInput
from django.conf import settings

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingFilterForm(forms.Form):
    location = forms.ChoiceField(choices=[], required=True)
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    min_price = forms.IntegerField(required=False, label="Min Price", initial=100, 
                                   widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}))
    max_price = forms.IntegerField(required=False, label="Max Price", initial=45000, 
                                   widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}))
    
    rating_choices = [(i, f"{i} Stars") for i in range(1, 11)]
    min_rating = forms.ChoiceField(choices=rating_choices, required=False, label="Minimum Rating", initial=1)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        sorted_l = Hotel.objects.values_list('location', flat=True).distinct().order_by('location')
        self.fields['location'].choices = [(loc, loc) for loc in sorted_l]

class BookingConfirmationForm(forms.Form):
    check_in = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        room_choices = [(room.room_type, room.room_type) for room in Room.objects.all()]
        self.fields['room_type'] = forms.ChoiceField(choices=room_choices, label='Room Type')


        #sort
        sorted_l = Hotel.objects.all().order_by('location')
        location_choices = [(hotel.location, hotel.location) for hotel in sorted_l]
        self.fields['location'] = forms.ChoiceField(choices=location_choices, label='Location')

    price_per_night = forms.DecimalField(max_digits=10, decimal_places=2, label='Price Per Night')
    rating = forms.DecimalField(max_digits=2, decimal_places=1, label='Rating (out of 10)', min_value=0, max_value=10)