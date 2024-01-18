from django.contrib import admin
from .models import Category, Seller, Product, Customer, Order, OrderItem

admin.site.register([Category, Seller, Product, Customer, Order, OrderItem])

