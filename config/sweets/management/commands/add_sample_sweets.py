"""
Django management command to add sample sweets data
Usage: python manage.py add_sample_sweets
"""
from django.core.management.base import BaseCommand
from sweets.models import Sweet
import uuid


class Command(BaseCommand):
    help = 'Adds sample sweets data to the database'

    def handle(self, *args, **options):
        sweets_data = [
            {
                'name': 'Ladoo',
                'category': 'Indian Sweets',
                'price': 100.00,
                'quantity': 10,
                'description': 'Traditional Indian sweet made from gram flour.'
            },
            {
                'name': 'Gulab Jamun',
                'category': 'Indian Sweets',
                'price': 120.00,
                'quantity': 15,
                'description': 'Soft milk-solid balls soaked in sugar syrup.'
            },
            {
                'name': 'Rasgulla',
                'category': 'Indian Sweets',
                'price': 110.00,
                'quantity': 20,
                'description': 'Spongy cottage cheese balls in sugar syrup.'
            },
            {
                'name': 'Jalebi',
                'category': 'Indian Sweets',
                'price': 80.00,
                'quantity': 25,
                'description': 'Crispy orange-colored sweet pretzels soaked in sugar syrup.'
            },
            {
                'name': 'Barfi',
                'category': 'Indian Sweets',
                'price': 150.00,
                'quantity': 12,
                'description': 'Dense milk-based sweet with various flavors.'
            },
            {
                'name': 'Kaju Katli',
                'category': 'Premium Sweets',
                'price': 200.00,
                'quantity': 8,
                'description': 'Diamond-shaped cashew fudge.'
            },
            {
                'name': 'Peda',
                'category': 'Indian Sweets',
                'price': 130.00,
                'quantity': 18,
                'description': 'Soft, milk-based sweet with cardamom flavor.'
            },
            {
                'name': 'Mysore Pak',
                'category': 'South Indian Sweets',
                'price': 140.00,
                'quantity': 14,
                'description': 'Rich, ghee-laden sweet from South India.'
            },
            {
                'name': 'Soan Papdi',
                'category': 'Indian Sweets',
                'price': 90.00,
                'quantity': 22,
                'description': 'Flaky, layered sweet with a melt-in-mouth texture.'
            },
            {
                'name': 'Rasmalai',
                'category': 'Premium Sweets',
                'price': 160.00,
                'quantity': 10,
                'description': 'Soft cheese patties in sweetened, thickened milk.'
            },
            {
                'name': 'Modak',
                'category': 'Indian Sweets',
                'price': 100.00,
                'quantity': 16,
                'description': 'Sweet dumplings filled with coconut and jaggery.'
            },
            {
                'name': 'Chikki',
                'category': 'Indian Sweets',
                'price': 70.00,
                'quantity': 30,
                'description': 'Brittle made from nuts and jaggery or sugar.'
            },
            {
                'name': 'Balushahi',
                'category': 'Indian Sweets',
                'price': 95.00,
                'quantity': 20,
                'description': 'Flaky, glazed doughnut-like sweet.'
            },
            {
                'name': 'Kheer',
                'category': 'Indian Sweets',
                'price': 85.00,
                'quantity': 15,
                'description': 'Rice pudding with milk, sugar, and cardamom.'
            },
            {
                'name': 'Imarti',
                'category': 'Indian Sweets',
                'price': 75.00,
                'quantity': 25,
                'description': 'Deep-fried, flower-shaped sweet in sugar syrup.'
            },
            {
                'name': 'Kalakand',
                'category': 'Indian Sweets',
                'price': 145.00,
                'quantity': 12,
                'description': 'Dense, milk-based sweet with a grainy texture.'
            },
            {
                'name': 'Petha',
                'category': 'Indian Sweets',
                'price': 60.00,
                'quantity': 35,
                'description': 'Candied ash gourd, translucent and sweet.'
            },
            {
                'name': 'Gajar Halwa',
                'category': 'Indian Sweets',
                'price': 125.00,
                'quantity': 10,
                'description': 'Carrot pudding cooked in milk and ghee.'
            },
            {
                'name': 'Milk Cake',
                'category': 'Premium Sweets',
                'price': 180.00,
                'quantity': 8,
                'description': 'Rich, fudge-like sweet made from milk solids.'
            },
            {
                'name': 'Lassi',
                'category': 'Beverages',
                'price': 50.00,
                'quantity': 40,
                'description': 'Yogurt-based drink, sweet or salty.'
            },
        ]

        created_count = 0
        skipped_count = 0

        for sweet_data in sweets_data:
            # Check if sweet already exists
            if Sweet.objects.filter(name=sweet_data['name']).exists():
                self.stdout.write(
                    self.style.WARNING(f'Skipping {sweet_data["name"]} - already exists')
                )
                skipped_count += 1
                continue

            # Create the sweet
            Sweet.objects.create(**sweet_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Added: {sweet_data["name"]}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully added {created_count} sweets!'
            )
        )
        if skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(f'Skipped {skipped_count} sweets (already exist)')
            )

