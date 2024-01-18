from django.core.management.base import BaseCommand
from myapp.models import Category, Seller, Product, Customer, Order, OrderItem
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))

        # Seed categories
        categories = ['Electronics', 'Clothing', 'Books', 'Home and Garden', 'Toys']
        for category_name in categories:
            Category.objects.create(name=category_name)

        # Seed sellers
        for _ in range(5):
            Seller.objects.create(name=fake.company(), email=fake.email())

        # Seed products
        for _ in range(20):
            product_category = random.choice(Category.objects.all())
            product_seller = random.choice(Seller.objects.all())
            Product.objects.create(
                name=fake.company(),  # Use company() for product names
                description=fake.text(),
                price=random.uniform(10, 1000),
                category=product_category,
                seller=product_seller
            )

        # Seed customers
        for _ in range(10):
            Customer.objects.create(username=fake.user_name(), email=fake.email())

        # Seed orders with order items
        for _ in range(10):
            customer = random.choice(Customer.objects.all())
            order = Order.objects.create(customer=customer, total_amount=0)

            for _ in range(random.randint(1, 5)):
                product = random.choice(Product.objects.all())
                quantity = random.randint(1, 10)
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
                order.total_amount += product.price * quantity

            order.save()

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))
