import os
import django

# 1. Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_project.settings')

# 2. Initialize Django
django.setup()

# 3. NOW you can import your models
from shop.models import Product


def update_product_details():
    updates = {
        'Vitamin C': {
            'benefits':
            'Supports immune system function and skin health. High in antioxidants.',
            'usage': 'Take 1 tablet daily with a meal.',
            'location': 'Nairobi Warehouse'
        },
        'Moringa': {
            'benefits':
            'Natural energy booster. Rich in vitamins A, C, and E, and essential minerals.',
            'usage': 'Mix 1 teaspoon into your morning smoothie or water.',
            'location': 'Nairobi Warehouse'
        },
        'Zinc': {
            'benefits':
            'Essential for DNA synthesis and immune health. Helps in wound healing.',
            'usage': 'Take 1 capsule daily after dinner.',
            'location': 'Nairobi Warehouse'
        },
        'Turmeric': {
            'benefits':
            'Contains Curcumin with powerful anti-inflammatory and antioxidant properties.',
            'usage': 'Add 1/2 teaspoon to warm milk or food twice daily.',
            'location': 'Mombasa Branch'
        },
        'Ginseng honey ginger': {
            'benefits':
            'Excellent for digestion, nausea relief, and natural stamina enhancement.',
            'usage': 'Steep one tea bag in hot water for 5 minutes.',
            'location': 'Nairobi Warehouse'
        }
    }

    print("--- Nutrientz Data Booster ---")
    for name, details in updates.items():
        # Match products by name
        products = Product.objects.filter(name__icontains=name)
        if products.exists():
            for p in products:
                p.benefits = details['benefits']
                p.usage = details['usage']
                p.location = details['location']
                p.save()
                print(f"✅ Updated: {p.name}")
        else:
            print(f"⚠️ Could not find: {name}")


if __name__ == '__main__':
    update_product_details()
