from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Menu(models.Model):
    items = models.CharField(max_length=200)
    price = models.IntegerField(max_length=100)

    def __str__(self):
        return self.items


class CartItem(models.Model):
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.items}"
