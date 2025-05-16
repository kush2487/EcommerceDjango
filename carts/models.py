from django.db import models
from products.models import Products
from django.contrib.auth.models import User
# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True) 

    # for view on the dasboard
    def __str__(self):
        return f"{self.user.username} - {self.products.name} ({self.quantity})"