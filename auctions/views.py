from asyncio.windows_events import NULL
from email import message
from itertools import product
from django import forms
from django.db import IntegrityError
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .form import auctionlisting_form
from django.contrib.auth.decorators import login_required
from .models import autionlisting,User,comment,wishlists




def index(request):
    items=autionlisting.objects.all()
    return render(request, "auctions/index.html",{
        "item":items
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
            a=request.user
            request.session['user']=a.id
            request.session['email']=a.email
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
        if password != confirmation or username=="" or email=="":
            return render(request, "auctions/register.html", {
                "message": "Passwords must match and all field must be filled."
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

def create(request):
    error=''
    items=autionlisting.objects.all()
    if request.method == 'GET':
        user=request.user
        try:
            if User.objects.get(username=user):
                context = {
                    'form': auctionlisting_form(), 
                }
                return render(request,'auctions/create.html', context)
        except:
                    return HttpResponseRedirect(reverse("login"))
    
    if request.method=='POST' :
        user=request.user
        a=auctionlisting_form(request.POST)
        if a.is_valid():
            name=request.POST.get('name')
            if autionlisting.objects.filter(name=name):
                return render(request,'auctions/index.html',{
                 "item":items
             })
            else:
                new_list=a.save(commit=False)
                new_list.created_user=request.user
                new_list.save()
                request.session['list']=new_list.id
        else:
            error="Fill all th details and please input date in YYYY-MM-DD format "
    items=autionlisting.objects.all()
    return render(request,"auctions/index.html",{
        "item":items,
        "error":error
    })

def product_page(request):
    present_user=request.user
    closed=0
    if request.method=='GET':
        id=request.GET.get('id')
        products=autionlisting.objects.get(id=id)
        comments=comment.Comment(products)
        product_creater=products.created_user
        same_user=None
        try: 
                
                if products.close_bid==1:
                    closed=1
        except:
                pass
        if present_user==product_creater:
            same_user=present_user
        products=autionlisting.objects.filter(id=id)

    if request.method=='POST':
        id=request.POST.get('id')
        products=autionlisting.objects.filter(id=id)
        try:
            current_user=request.user
            registered_user=User.objects.get(username=current_user)
            if registered_user:
                bid=request.POST.get('bid')
                bidder=registered_user.username
                products_to_edit=autionlisting.objects.get(id=id)
                products_to_edit.starting_bid=bid
                products_to_edit.bidder=bidder
                products_to_edit.save()
                
                
                
            
            product=autionlisting.objects.get(id=id)
            comments=comment.Comment(product)
            product_creater=product.created_user
            same_user=None
            if present_user==product_creater:
                same_user=present_user 
            try: 
                
                if product.bid==1:
                    closed=1
            except:

                pass
        except:
            return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/product_page.html",{
        "items":products,
        "same_user":same_user,
        "closed":closed,
        "comments":comments
        
    })
        
@login_required(login_url='/login')
def comments(request):
    closed=0
    user=request.user
    id=request.POST.get('id')
    text=request.POST.get('comment')
    user=User.objects.get(username=user)
    products=autionlisting.objects.get(id=id)
    if products.close_bid==1:
            closed=1
    same_user=None
    if user == products.created_user:
        same_user=user
    if user:
        if text:
            new_comment=comment.objects.create(user=user,product=products,comment=text)
            new_comment.save()
        else:
            pass
    comments=comment.Comment(products)
    products=autionlisting.objects.filter(id=id)
    return render(request,"auctions/product_page.html",{
        "items":products,
        "same_user":same_user,
        "comments":comments,
        "closed":closed
    })
@login_required(login_url='/login')
def whishlist(request):
    user_id=request.user
    closed=0
    alert=''
    message=''
    if request.method=='POST':
        product_id=request.POST.get('id')
        whishlist_product=wishlists.objects.filter(id=product_id)
        whishlist_product.delete()
        user=User.objects.get(username=user_id)
        
        items=wishlists.objects.filter(user=user)

        return render(request,"auctions/whishlist.html",{
                    "items":items,
                })
            


    id=request.GET.get('id')
    if id:
        user=User.objects.get(username=request.user)
        products=autionlisting.objects.filter(id=id)
        product=autionlisting.objects.get(id=id)
        try:
            already_exist= wishlists.objects.get(product=product ,user=user)
            alert="Item is already in Whishlist"
        except:
                whishlist=wishlists.objects.create(user=user,product=product)
                whishlist.save()
                message="Successfully added to Whishlist"
        same_user=None
        if product.close_bid==1:
            closed=1
        comments=comment.Comment(product)
        return render(request,"auctions/product_page.html",{
            "items":products,
            "same_user":same_user,
            "comments":comments,
            "closed":closed,
            "alert":alert,
            "message":message
        })
    user=User.objects.get(username=user_id)
    if user:
        items=wishlists.objects.filter(user=user)
        return render(request,"auctions/whishlist.html",{
            "items":items,
        })
    else:
        return render(request,"auctions/whishlist.html")
    
@login_required(login_url='/login')  
def close_bid(request):
    id=request.POST.get('id')
    products=autionlisting.objects.filter(id=id)
    close_bid=autionlisting.objects.get(id=id)
    close_bid.close_bid=1
    close_bid.save()
    closed="closed"
    return render(request,"auctions/product_page.html",{
            "items":products,
            "comments":comments,
            "closed":closed
        })
 
