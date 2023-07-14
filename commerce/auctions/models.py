from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.FloatField()
    imgURL = models.URLField()
    category = models.CharField(max_length=64)

class Bid(models.Model):
    bid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)