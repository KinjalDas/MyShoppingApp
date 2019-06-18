from django.db import models

# Create your models here.
from MyShop.models import Product
from django.core.exceptions import ValidationError

class Cart(models.Model):

    def check_quanity(value):
        if quantity>product.quantity:
            raise ValidationError("Sorry availability of "+ product.name +" is limited to :" + product.quantity)

    product = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField()
