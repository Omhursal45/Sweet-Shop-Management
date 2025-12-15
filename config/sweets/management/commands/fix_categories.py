"""
Django management command to fix duplicate/normalize categories
Usage: python manage.py fix_categories
"""
from django.core.management.base import BaseCommand
from sweets.models import Sweet


class Command(BaseCommand):
    help = 'Fixes and normalizes category names (removes duplicates, normalizes case)'

    def handle(self, *args, **options):
        # Category normalization mapping
        category_map = {
            'sweet': 'Indian Sweets',  # Fix lowercase 'sweet'
            'Sweet': 'Indian Sweets',  # Fix capitalized 'Sweet'
            'SWEET': 'Indian Sweets',  # Fix uppercase 'SWEET'
        }
        
        updated_count = 0
        
        for sweet in Sweet.objects.all():
            original_category = sweet.category
            normalized_category = category_map.get(original_category, original_category)
            
            # Also normalize common variations
            if normalized_category.lower() in ['sweet', 'sweets']:
                normalized_category = 'Indian Sweets'
            
            if normalized_category != original_category:
                sweet.category = normalized_category
                sweet.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated: {sweet.name} - "{original_category}" -> "{normalized_category}"')
                )
        
        if updated_count == 0:
            self.stdout.write(self.style.SUCCESS('No categories needed fixing.'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\nFixed {updated_count} category entries!')
            )
        
        # Show final category list
        categories = sorted(set(Sweet.objects.values_list('category', flat=True)))
        self.stdout.write(f'\nCurrent unique categories: {categories}')

