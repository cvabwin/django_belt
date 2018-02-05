## encoding:utf-8--
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Wish

def index(request):
    return render(request, "wish_list_app/index.html")

def wish_list(request):
    if "user_id" not in request.session:
        return redirect("/")

    # Variable to hold all wishes
    otherWishes = Wish.objects.all()

    # Variable to hold all the user with wishes
    userWishes = User.objects.get(id=request.session["user_id"]).wishes.all()

    #Using a for loop to exclude all the wishes except the ones favored by the user in session
    for wishes in userWishes:
        otherWishes = otherWishes.exclude(id=wishes.id)
    data = {

        "wishes": otherWishes,
        "this_user": User.objects.get(id=request.session["user_id"]),
    }
    return render(request, "wish_list_app/wish_list.html", data)

def register(request):
    response = User.objects.register(
        name=request.POST["name"],
        username=request.POST["username"],
        date_hired=request.POST["date_hired"],
        password=request.POST["password"],
        confirm_password=request.POST["confirm_password"]
    )
    
    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'You successfully logged in!')
        request.session["user_id"] = response["user"].id
        request.session["name"] = response["user"].name
        request.session["username"] = response["user"].username

        return redirect("/wish_list")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def login(request):
    response = User.objects.login(
        username=request.POST["username"],
        password=request.POST["password"]
    )

    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'You successfully logged in!')
        request.session["user_id"] = response["user"].id
        request.session["name"] = response["user"].name
        request.session["username"] = response["user"].username
        return redirect("/wish_list")

    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def new(request):
    return render(request, "wish_list_app/create.html")

def create_wish(request):
    this_user = User.objects.get(id=request.session["user_id"])
    wishes = Wish.objects.create(
        wish = request.POST["wish_item"],
        posted_by_id = request.session["user_id"]
    )
   #print wish.author, wish.message
    return redirect("/wish_list")

def add_wish(request, id):
    this_wish = Wish.objects.get(id=id)
    this_user = User.objects.get(id=request.session["user_id"])
    this_wish.users_wishing.add(this_user)
    return redirect("/wish_list")

def remove_wish(request, id):
    this_wish = Wish.objects.get(id=id)
    this_user = User.objects.get(id=request.session["user_id"])
    this_wish.users_wishing.remove(this_user)
    return redirect("/wish_list")

def delete_wish(request, id):
    this_wish = Wish.objects.get(id=id)
    this_user = User.objects.get(id=request.session["user_id"])
    this_wish.delete()
    return redirect("/wish_list")

def display_item(request, id):
    
    data = {
        "wishes": Wish.objects.all(),
        "this_wish": Wish.objects.get(id=id),
        "users": User.objects.all(),
        "this_user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "wish_list_app/display_item.html", data)

 