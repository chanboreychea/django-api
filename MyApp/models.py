import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    createBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updateBy = models.IntegerField(null=True)
    createAt = models.DateField(auto_now_add=datetime.datetime.now())
    updateAt = models.DateField(null=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    barcode = models.IntegerField(unique=True, null=False)
    unitPrice = models.FloatField(null=False)
    qtyInstock = models.IntegerField(null=False)
    photo = models.ImageField(upload_to="media/", null=False)
    createBy = models.ForeignKey(User, on_delete=models.CASCADE)
    updateBy = models.IntegerField(null=True)
    createAt = models.DateField(auto_now_add=datetime.datetime.now())
    updateAt = models.DateField(null=True)


class Purchase(models.Model):
    purchaseDate = models.DateField(auto_now_add=datetime.datetime.now())
    createBy = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    cost = models.FloatField()
    total = models.FloatField()


class Sale(models.Model):
    saleDate = models.DateField(auto_now_add=datetime.datetime.now())
    createBy = models.ForeignKey(User, on_delete=models.CASCADE)
    totalAmount = models.FloatField()


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
