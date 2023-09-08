from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count

from .models import User, AuctionListing, Bid, Watchlist


def index(request):

    # Get the active listings
    listings = AuctionListing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
    })


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
        # Take the data from the form
        
        author = request.user
        title = request.POST['title']
        description = request.POST['description']
        start_bid = request.POST['start_bid']

        img_url = request.POST['img_url']
        category = request.POST['category']

        # Attempt to create a listing
        try:
            listing = AuctionListing(
                author=author,
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
            "message": "Listing succesfully created",
            "listings": AuctionListing.objects.all()
        })
    else:
        return render(request, "auctions/create.html")
    

def show_listing(request, id):
    
    # Get the listing with the passed id
    listing = AuctionListing.objects.get(listing_id=id)

    # Get the bids associated with the listing
    bid = Bid.objects.filter(listing_id=id).order_by('amount').last()

    # Render the listing
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "last_bid": bid
    })

def create_bid(request):
    
    if request.method == 'POST':

        # Get data from the request to check is correct
        amount = float(request.POST['amount'])
        id = request.POST['listing_id']
        user = request.user   
        listing = AuctionListing.objects.get(listing_id=id)

        # Get the last bid associated with this listing
        last_bid = Bid.objects.filter(listing_id=id).order_by('amount').last()

        if amount > last_bid.amount:
            
            # Create and save bid
            bid = Bid(amount=amount, user=user, listing_id=listing)
            bid.save()

            return redirect('listing', id=id)
        else:
            return render(request, "auctions/listing.html", {
                'message': "ERROR: The bid needs to be higher than the actual one",
                "listing": listing,
                "last_bid": last_bid
            })
        
def show_categories(request):
    
    if request.method == "POST":
        # Get the category listings
        listings = AuctionListing.objects.get(request.POST['category'])

        return render(request, "auctions/index.html", {
            "listings": listings
        })
    else:

        categories = AuctionListing.objects.values('category').annotate(count=Count('category'))

        return render(request, "auctions/categories.html", {
            "categories": categories
        })

        
def add_to_watchlist(request):
    if request.method == "POST":
        # TODO: Add to watchlist
        user = request.user
        listing = AuctionListing.objects.get(listing_id=request.POST['listing_id'])

        watchlist = Watchlist(user, listing)
        watchlist.save()
    else:
        # Get the active listings
        watchlist = Watchlist.objects.get(user=request.user)
        print(watchlist)

        #return render(request, "auctions/index.html", {
        #    "listings": listings
        #})