from django.db import models
from decimal import Decimal
from django.conf import settings



class Cart(models.Model):
    TotalPay=models.FloatField(default=0)
    ItemsNumber = models.IntegerField(max_length=100, default=0)
    UserId=models.IntegerField(default=0)
    ItemsId=models.CharField(max_length=1000,default=" ")

    def __str__(self):
        return str(self.TotalPay)



class Category(models.Model):
    CategoryName = models.CharField(max_length=200)

    def __str__(self):
        return self.CategoryName


class Item(models.Model):
    ItemName = models.CharField(max_length=200)
    ItemPrice = models.CharField(max_length=200)
    ItemRate = models.FloatField(max_length=400, default=0.0)
    ItemDetails=models.CharField(max_length=1000 ,default="Nothing")
    ItemCategory = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    ItemLogo = models.ImageField(upload_to='products/', null=True, blank=True)
    stars=models.CharField(max_length=5,null=True,default='',blank=True)
    graystars=models.CharField(max_length=5,null=True,default='xxxxx')

    def __str__(self):
        return self.ItemName + ' - ' + self.ItemPrice



class Comment(models.Model):
    Review= models.TextField(max_length=3000)
    Rate = models.IntegerField(default=0)
    #variables btd5ol fl database ka dictionary
    itemId = models.IntegerField(default=0)
    username= models.CharField(max_length=200)
    stars=models.CharField(max_length=5,null=True,default='',blank=True)
    graystars=models.CharField(max_length=5,null=True,default='xxxxx')


