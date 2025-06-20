from django.core.management.base import BaseCommand
from data.models import Plant
from django.core.files.base import ContentFile
import random
from pathlib import Path
from django.core.files import File

class Command(BaseCommand):
    help = 'Add sample plant data to the database.'

    def handle(self, *args, **options):
        image_dir = Path('media/plants')
        image_files = {
            'Aloe Vera': 'plant2.jpg',
            'Rose': 'plant3.jpg',
            'Basil': 'plat01.jpg',
            'Ficus': 'plant2.jpg', # Using placeholder, replace with actual image
            'Cactus': 'plant3.jpg' # Using placeholder, replace with actual image
        }

        sample_plants = [
            {
                'name': 'Aloe Vera',
                'Desciption': 'A succulent plant species of the genus Aloe.',
                'Category': 'Succulent',
                'Quantity': 20,
                'price': 150.00,
            },
            {
                'name': 'Rose',
                'Desciption': 'A woody perennial flowering plant of the genus Rosa.',
                'Category': 'Flowering',
                'Quantity': 15,
                'price': 200.00,
            },
            {
                'name': 'Basil',
                'Desciption': 'A culinary herb of the family Lamiaceae.',
                'Category': 'Herb',
                'Quantity': 30,
                'price': 50.00,
            },
            {
                'name': 'Ficus',
                'Desciption': 'A genus of about 850 species of woody trees.',
                'Category': 'Indoor',
                'Quantity': 10,
                'price': 350.00,
            },
            {
                'name': 'Cactus',
                'Desciption': 'A member of the plant family Cactaceae.',
                'Category': 'Cactus',
                'Quantity': 25,
                'price': 120.00,
            },
        ]

        for plant_data in sample_plants:
            image_name = image_files.get(plant_data['name'])
            image_path = image_dir / image_name if image_name else None

            plant, created = Plant.objects.get_or_create(
                name=plant_data['name'],
                defaults={
                    'Desciption': plant_data['Desciption'],
                    'Category': plant_data['Category'],
                    'Quantity': plant_data['Quantity'],
                    'price': plant_data['price'],
                }
            )

            if created:
                if image_path and image_path.exists():
                    with open(image_path, 'rb') as f:
                        plant.image.save(image_name, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"Added plant: {plant.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Plant already exists: {plant.name}"))
        self.stdout.write(self.style.SUCCESS('Sample plant data insertion complete.'))

BASE_DIR = Path(__file__).resolve().parent.parent 