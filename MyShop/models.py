from django.db import models
from django.core.exceptions import ValidationError
from MyAccounts.models import *

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    desc = models.CharField(max_length=50)
    image = models.ImageField(upload_to='MyShop/products_images',blank=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProductPair(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    shop_quant = models.PositiveIntegerField()

    def __str__(self):
        return "{0} , {1}".format(self.product.name,self.shop_quant)

class Cart(models.Model):
    products = models.ManyToManyField(ProductPair)

class Order(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "{0} , {1} ,{2}".format(self.user.user.username,self.product.name,self.quantity)
