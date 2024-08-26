from django.core.management.base import BaseCommand
from django_seed import Seed
from hotels.models import Hotel, Room, Booking

class Command(BaseCommand):
    help = 'Seed the database with hotel data'

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        seeder.add_entity(Hotel, 5, {
            'name': lambda x: seeder.faker.company(),
            'location': lambda x: seeder.faker.city(),
            'description': lambda x: seeder.faker.text(),
            'rating': lambda x: round(seeder.faker.random.uniform(1.0, 10.0), 1),
            'amenities': lambda x: seeder.faker.words(nb=5),
            'image': None,  # Leave None if you don't want to seed images
        })

        seeder.add_entity(Room, 3, {
            'hotel': lambda x: Hotel.objects.order_by('?').first(),
            'room_type': lambda x: seeder.faker.word(),
            'price_per_night': lambda x: round(seeder.faker.random.uniform(50, 500), 2),
            'availability': lambda x: seeder.faker.boolean(),
        })

        inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))