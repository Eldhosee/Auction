from itertools import product
from pickle import TRUE
from pydoc import describe
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class categorylist(models.Model):
    category=models.CharField(max_length=30, default='')

    def __str__(self):
        return f"{self.category}"

class autionlisting(models.Model):
    name=models.CharField(max_length=30)
    starting_bid=models.IntegerField(null=True,default=1)
    category=models.ForeignKey(categorylist,on_delete=models.CASCADE,related_name="category_list_name",blank=True,null=True)
    image=models.URLField(null=True,default='')
    description=models.TextField(null=True,default='')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_user",blank=True,null=True)
    close_bid=models.BooleanField(default=0)
    bidder=models.CharField(max_length=300,null=True,default='')
    end_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.name}"
    
    def IsExist(self):
        if autionlisting.objects.filter(name=self.name):
            return True
        else:
            False


class comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True )
    product=models.ForeignKey(autionlisting,on_delete=models.CASCADE,blank=True,null=True)
    comment=models.TextField()

    def __str__(self):
        return f"{self.user}:{self.comment}"
    def Comment(products):
        return reversed(comment.objects.filter(product=products).reverse())


class wishlists(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(autionlisting,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.product}"