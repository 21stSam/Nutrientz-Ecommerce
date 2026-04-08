import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Imports full client hierarchy with specific product examples'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Full Hierarchy: { Parent: { Sub-Category: [Product Examples] } }
        full_data = {
            "Nutrients": {
                "Vitamins": ["Vitamin ADEK", "Vitamin B complex", "Vitamin C"],
                "Minerals": ["Calcium"],
                "Antioxidants": ["Co q10", "Zinc", "Selenium"],
                "Protein (amino acids)": ["Collagen", "Glutathion"],
                "Omega (fatty acids)": [],  # Empty list creates category only
                "Probiotics & enzymes": [],
                "Fiber & prebiotic": [],
            },
            "Plant-based nutrients": {
                "Phytonutrients": []
            },
            "Botanicals": {
                "Herbal extracts":
                ["Gingkgo", "Garlic", "Turmeric", "Moringa"],
                "Ayurvedic & traditional herbs": ["Maca", "Brahmi"],
                "Herbal teas": [],
                "Herb-infused coffees": [],
                "Herbal infusions": ["Ginseng honey ginger"],
                "Herbal juices": ["Aloe vera juice"],
            },
            "Women’s wellness": {
                "Pregnancy (preconception & postnatal)": [],
                "Menopause": [],
                "Women's Multivitamins & minerals": [],
            },
            "Kids wellness": {
                "Multivitamins & minerals for baby": [],
                "Child wellness": [],
                "Teen wellness": [],
            },
            "Men’s wellness": {
                "Grooming": [],
                "Sexual health": [],
                "Men's Multivitamins & minerals": [],
            },
            "Personal care": {
                "Face & skin": [],
                "Oral & lips": [],
                "Intimate care": [],
            },
            "Body system": {
                "Hair, nail & skin": [],
                "Immunity": [],
                "Bone, joint & mobility": [],
                "Circulation (heart, brain, memory)": [],
                "Vision": [],
            },
            "Health goal": {
                "Weight management": [],
                "Anti-aging": [],
                "Stress & sleep support": [],
                "Detox & cleanse": [],
            }
        }

        for parent_name, subs in full_data.items():
            parent_cat = Category.objects.create(name=parent_name,
                                                 slug=slugify(parent_name))
            self.stdout.write(self.style.SUCCESS(f'Parent: {parent_name}'))

            for sub_name, products in subs.items():
                sub_cat = Category.objects.create(name=sub_name,
                                                  slug=slugify(sub_name),
                                                  parent=parent_cat)
                self.stdout.write(f'  - Sub: {sub_name}')

                # Add specific examples as products
                for prod_name in products:
                    price = Decimal(random.randint(1500, 5000))
                    Product.objects.create(
                        category=sub_cat,
                        name=prod_name,
                        slug=slugify(prod_name),
                        description=
                        f"Premium {prod_name} formulated for optimal health.",
                        price=price,
                        stock=random.randint(5, 20),
                        available=True)
                    self.stdout.write(f'    * Product: {prod_name}')

        self.stdout.write(
            self.style.SUCCESS('Nutrientz full structure is live!'))
