from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.name)

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default = 0)
    is_available = models.BooleanField(default=False)

    category = models.ForeignKey(
        'Category', 
        on_delete=models.CASCADE,
        related_name='products',
        null= True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" {self.name} |  {self.price} |  {self.description} "  
