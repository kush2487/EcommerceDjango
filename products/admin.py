from django.contrib import admin
from products.models import Products, Category

# Register your models here.
admin.site.register(Products)
admin.site.register(Category)