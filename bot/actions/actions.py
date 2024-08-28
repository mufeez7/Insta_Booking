# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
import arrow 
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from django.core.exceptions import ObjectDoesNotExist
from hotels.models import Hotel, Room, Booking
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

city_db = {
    'brussels': 'Europe/Brussels', 
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'Amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific'
}

class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        print(current_place)
        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place."
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
                
        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)
        
        return []

class ActionCheckRoomAvailability(Action):
    def name(self) -> Text:
        return "action_check_room_availability"
    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotel_name = tracker.get_slot("hotel_name")
        print(hotel_name)

        if hotel_name is None:
            dispatcher.utter_message(text="Please specify the hotel name.")
            return []
        
        try:
            
            hotel =  Hotel.objects.get(name__iexact=hotel_name)
            available_rooms =  Room.objects.filter(hotel=hotel, availability=True)

            if available_rooms.exists():
                response = f"Yes, rooms are available at {hotel_name}."
            else:
                response = f"Sorry, no rooms are available at {hotel_name}."

            dispatcher.utter_message(text=response)
        except ObjectDoesNotExist:
            dispatcher.utter_message(text=f"Hotel {hotel_name} not found.")
        
        return []

class ActionCancelBooking(Action):
    def name(self) -> Text:
        return "action_cancel_booking"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotel_name = tracker.get_slot("hotel_name")
        user_id = tracker.sender_id  
        print(hotel_name, ' ', user_id)

        if not hotel_name:
            dispatcher.utter_message(text="Please specify the hotel name for which you want to cancel the booking.")
            return []

        try:
            bookings = Booking.objects.filter(user_id=user_id)  
            
            if bookings.exists():  

                booking_options = []

                for booking in bookings:
                    booking_options.append(f"Booking ID: {booking.id}, Hotel: {booking.room.hotel.name}")

                booking_list_message = "\n".join(booking_options)
                dispatcher.utter_message(text=f"You have the following bookings:\n{booking_list_message}\nPlease specify the Booking ID of the one you want to cancel.")

            else:
                dispatcher.utter_message(text=f"No booking found for {hotel_name} under your name.")

        except Booking.DoesNotExist:
            dispatcher.utter_message(text=f"Hotel {hotel_name} not found.")
        
        return []
    
class ActionIDCancel(Action):
    def name(self) -> Text:
        return "action_id_cancel"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        booking_id = tracker.get_slot("booking_id")
        user_id = tracker.sender_id

        if not booking_id:
            dispatcher.utter_message(text="Please provide the Booking ID you want to cancel.")
            return []

        try:
            booking = Booking.objects.get(id=booking_id, user_id=user_id)
            booking.room.availability = True
            booking.room.save()
            booking.delete()
        
            dispatcher.utter_message(text=f"Your booking with ID {booking_id} has been successfully canceled.")

        except Booking.DoesNotExist:
            dispatcher.utter_message(text=f"No booking found with ID {booking_id} under your account.")

        return []