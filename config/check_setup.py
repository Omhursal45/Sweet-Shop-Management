"""
Quick setup checker for Sweet Shop
Run this to check if everything is set up correctly
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from sweets.models import Sweet
from accounts.models import User

print("=" * 50)
print("SWEET SHOP SETUP CHECKER")
print("=" * 50)
print()

# Check Database Connection
print("1. Checking Database Connection...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("   ✓ Database connection successful")
except Exception as e:
    print(f"   ✗ Database connection failed: {e}")
    sys.exit(1)

# Check Migrations
print("\n2. Checking Migrations...")
try:
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('showmigrations', 'sweets', stdout=out, no_color=True)
    migrations = out.getvalue()
    
    if '[X]' in migrations or '0002' in migrations:
        print("   ✓ Migrations appear to be applied")
    else:
        print("   ⚠ Some migrations may not be applied")
        print("   Run: python manage.py migrate")
except Exception as e:
    print(f"   ⚠ Could not check migrations: {e}")

# Check Model Fields
print("\n3. Checking Model Fields...")
try:
    fields = [f.name for f in Sweet._meta.get_fields()]
    required_fields = ['name', 'category', 'price', 'quantity', 'description', 'image']
    
    missing_fields = [f for f in required_fields if f not in fields]
    if missing_fields:
        print(f"   ✗ Missing fields: {missing_fields}")
        print("   Run: python manage.py migrate")
    else:
        print("   ✓ All required fields present")
except Exception as e:
    print(f"   ✗ Error checking fields: {e}")

# Check Users
print("\n4. Checking Users...")
try:
    user_count = User.objects.count()
    staff_count = User.objects.filter(is_staff=True).count()
    print(f"   ✓ Total users: {user_count}")
    print(f"   ✓ Staff users: {staff_count}")
    
    if staff_count == 0:
        print("   ⚠ No staff users found!")
        print("   To add products, you need a staff user.")
        print("   Run: python manage.py createsuperuser")
        print("   Or make existing user staff in Django shell")
except Exception as e:
    print(f"   ✗ Error checking users: {e}")

# Check Products
print("\n5. Checking Existing Products...")
try:
    product_count = Sweet.objects.count()
    print(f"   ✓ Total products: {product_count}")
    
    if product_count == 0:
        print("   ℹ No products yet. You can add them after setup is complete.")
except Exception as e:
    print(f"   ✗ Error checking products: {e}")

# Check Pillow
print("\n6. Checking Pillow (for image uploads)...")
try:
    import PIL
    print("   ✓ Pillow is installed")
except ImportError:
    print("   ✗ Pillow is NOT installed")
    print("   Run: pip install Pillow")

print("\n" + "=" * 50)
print("SETUP CHECK COMPLETE")
print("=" * 50)
print("\nNext steps:")
print("1. If migrations are missing, run: python manage.py migrate")
print("2. If no staff user, run: python manage.py createsuperuser")
print("3. If Pillow missing, run: pip install Pillow")
print("4. Start server: python manage.py runserver")
print("5. Login and go to: http://127.0.0.1:8000/sweet/add/")

