from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        # TODO: Take the sent form and create the listing
        # Take the data from the form
        
        title = request.POST['title']
        description = request.POST['description']
        start_bid = request.POST['start_bid']

        img_url = request.POST['img_url']
        category = request.POST['category']

        # Attempt to create a listing
        try:
            listing = AuctionListing(
                title=title, 
                description=description, 
                starting_bid=start_bid, 
                imgURL=img_url,
                category=category
            )
            listing.save()
        except Exception as e:
            return render(request, "auctions/index.html", {
                "message": e
            })

        return render(request, "auctions/index.html", {
            "message": "Listing succesfully created"
        })
    else:
        return render(request, "auctions/create.html")