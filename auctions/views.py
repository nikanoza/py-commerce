from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    actives = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": actives,
        "categories": categories
    })

def createListing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["imageUrl"]
        price = request.POST["price"]
        category = request.POST["category"]
        categoryData = Category.objects.get(name=category)
        user = request.user
        bid = Bid(bid=int(price), user=user)
        bid.save()
        listing = Listing(title=title, description=description, imageUrl=image_url, price=bid, owner=user, active=True, category=categoryData)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
       
def filter_categories(request):
    if request.method == "POST":
        category = request.POST["category"]
        categories = Category.objects.all()
        if category == "all":
            listings = Listing.objects.all()
            return render(request, "auctions/index.html", {
                "listings": listings,
                "categories": categories
            })
        else:
            listings = Listing.objects.filter(active=True, category__name=category)
            return render(request, "auctions/index.html", {
                "listings": listings,
                "categories": categories
            })

def listing(request, id):
    if request.method == "GET":
        listing = Listing.objects.get(id=float(id))
        comments = Comment.objects.filter(listing=listing)
        isWachlist = request.user in listing.watchist.all()
        isOwner = request.user.username == listing.owner.username
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "isWatchlist": isWachlist,
            "comments": comments,
            "isOwner": isOwner
        })

def make_bid(request, id):
    currentBid = request.POST["bid"]
    listing = Listing.objects.get(id=float(id))
    if int(currentBid) > listing.price.bid:
        user = request.user
        newBid = Bid(bid=int(currentBid), user=user)
        newBid.save()
        listing.price = newBid
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    
def close_auction(request, id):
    listing = Listing.objects.get(id=float(id))
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))

def add_comment(request, id):
    if request.method == "POST":
        user = request.user
        comment = request.POST["comment"]
        listing = Listing.objects.get(pk=id)
        newComment = Comment(author=user,listing=listing,message=comment)
        newComment.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist(request):
    if request.method == "GET":
        listings = []
        listingData = Listing.objects.all()   
        user = request.user
        for listing in listingData:
            if user in listing.watchist.all():
                listings.append(listing)
        return render(request, "auctions/watchlist.html", {
            "listings": listings,
        })        

def remove_from_listing(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchist.remove(user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def add_to_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchist.add(user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

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
