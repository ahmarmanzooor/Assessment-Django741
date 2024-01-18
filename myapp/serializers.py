from rest_framework import serializers
from .models import Category, Product, Seller
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Product
        fields = ['name','description','price','category','seller']