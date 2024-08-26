import random
from django.core.management.base import BaseCommand
from hotels.models import Hotel

class Command(BaseCommand):
    help = "Randomly assigns hotel descriptions and amenities to Hotel model"

    DESCRIPTIONS = [
        "Nestled in the heart of the city, this luxurious hotel offers unparalleled comfort and style. Guests can indulge in well-appointed rooms, state-of-the-art amenities, and exceptional service, making it the perfect retreat for both leisure and business travelers.",
        "Experience the charm and intimacy of this boutique hotel, where every detail is designed to create a memorable stay. From uniquely decorated rooms to personalized service, guests will find a warm and welcoming atmosphere in this hidden gem.",
        "Located in the bustling downtown area, this contemporary hotel provides a sleek and stylish environment for guests. With modern amenities, spacious rooms, and easy access to the city's top attractions, it's the ideal base for exploring the urban landscape.",
        "Overlooking the pristine shoreline, this beachfront hotel offers stunning ocean views and direct access to sandy beaches. Guests can relax in elegantly furnished rooms, enjoy fresh seafood at the on-site restaurant, and unwind with a cocktail by the pool.",
        "Perfect for families, this resort offers a range of activities and amenities to keep everyone entertained. Spacious rooms, kid-friendly dining options, and a variety of recreational facilities make it an ideal destination for a fun-filled vacation.",
        "Step back in time at this historic hotel, where classic architecture meets modern luxury. Guests can immerse themselves in the rich history of the property while enjoying top-notch amenities and service in a truly unique setting.",
        "Surrounded by breathtaking mountain views, this cozy lodge provides a rustic yet comfortable retreat for nature lovers. Guests can enjoy outdoor activities, warm up by the fireplace, and savor hearty meals in a peaceful, serene environment.",
        "Designed with the business traveler in mind, this elegant hotel offers convenient amenities such as high-speed internet, meeting rooms, and a business center. Comfortable rooms and a central location make it easy to balance work and relaxation.",
        "This eco-friendly hotel is committed to sustainability without compromising on comfort. Guests can enjoy beautifully designed rooms made from natural materials, organic dining options, and environmentally conscious practices throughout their stay.",
    ]

    AMENITIES = [
        "Free Wi-Fi", "24-hour front desk", "Swimming pool", "Spa and wellness center",
        "Fitness center", "Restaurant", "Bar", "Airport shuttle", "Room service", 
        "Concierge service", "Free parking", "Business center", "Laundry service"
    ]

    def handle(self, *args, **kwargs):
        hotels = Hotel.objects.all()

        for hotel in hotels:
            hotel.description = random.choice(self.DESCRIPTIONS)

            random_amenities = random.sample(self.AMENITIES, k=random.randint(3, 8))
            hotel.amenities = ", ".join(random_amenities)

            hotel.save()

        self.stdout.write(self.style.SUCCESS('Successfully assigned descriptions and amenities to all hotels'))
