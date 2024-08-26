import pandas as pd
from django.core.management.base import BaseCommand
from hotels.models import Hotel, Room, Booking

data = pd.read_csv("C:/Users/mufeezur.rehman/Desktop/Hotel Kaggle Dataset/booking_hotel.csv", encoding='ISO-8859-1')
data = data.drop(columns=['Review Score', 'Number of   ', 'Room    Score', 'Bed Type'])

data['price'] = data['Room Price (in BDT or any other currency)'].astype(str)
data = data.drop(columns=['Room Price (in BDT or any other currency)'])
data['price'] = data['price'].str.replace(',', '', regex=True)
data['price'] = data['price'].astype(int)
conversion = 0.0084
data['price'] = data['price'] * conversion

data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
print(data['Rating'].isna().sum())  

data = data.dropna(subset=['Rating'])
data['Rating'] = data['Rating'].round().astype(int)


class Command(BaseCommand):
    help = 'Import data from a DataFrame into Django models'

    def handle(self, *args, **kwargs):
        # Process and import Hotel data
        for _, row in data.iterrows():
            hotel, created = Hotel.objects.get_or_create(
                name=row['Hotel Name'],
                defaults={
                    'location': row['Location'],
                    #'description': row['description'],
                    'rating': row['Rating'],
                    #'amenities': row['amenities'],
                }
            )
            if not created:
                # Update existing hotel
                hotel.location = row['Location']
                #hotel.description = row['description']
                hotel.rating = row['Rating']
                #hotel.amenities = row['amenities']
                hotel.save()

            # If you also have Room and Booking data, you can process it similarly
            # Example:
            room = Room(
                hotel=hotel,
                room_type=row['Room Type'],
                price_per_night=row['price'],
                #availability=row['availability']
            )
            room.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))