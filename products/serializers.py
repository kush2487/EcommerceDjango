from rest_framework import serializers
from products.models import Products, Category




class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = "category.name", read_only = True)
    class Meta:
        model = Products
        fields = '__all__'
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'