from turtle import title
from unicodedata import category, name
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    startBid = models.IntegerField()
    image = models.ImageField(upload_to='auction_images')
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    amount = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)