# serializers.py

from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

        
class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField()
    is_discount_active = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'cost', 'in_stock',
            'category', 'discount_percentage', 'discount_start',
            'discount_end', 'discounted_price', 'is_discount_active',
            'created_at', 'updated_at', 'is_active'
        ]

        
    def validate_category(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Selected category is not active.")
        return value