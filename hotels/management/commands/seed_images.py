import os
import random
import pandas as pd
from django.core.management.base import BaseCommand
from hotels.models import Hotel
from django.conf import settings


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
    help = 'Seed the Hotel model with data from a DataFrame and random images'

    def handle(self, *args, **kwargs):

        image_files = [
            'metropol.jpg',
            'miami_stock.jpg',
            'st-regis-hotel-nyc-usa-2A109CP.jpg',
            'the-st-regis-aspen-resort.jpg',
            'bali_one.jpg',
            'bali_two.jpg',
            'bang_one.jpg',
            'shang_one.jpg',
            'tokyo_one.jpg',
        ]
        image_folder = 'hotel_images/'

        for index, row in data.iterrows():

            image_file = random.choice(image_files)
            image_path = os.path.join(settings.MEDIA_ROOT, image_folder, image_file)
            image_url = os.path.join(image_folder, image_file)

            hotel, created = Hotel.objects.update_or_create(
                name=row['Hotel Name'],
                defaults={
                    'image': image_url 
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created hotel {hotel.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated hotel {hotel.name}'))
