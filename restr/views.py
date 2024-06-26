from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # for flash messages
from django.urls import reverse
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from .models import Menu, CartItem
from django.views import generic


# Create your views here.


def index(request):
    menus = Menu.objects.all()
    return render(request, "restr/index.html", {"menus": menus})


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    # price = (item.product.price * item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(
        request,
        "restr/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


def add_to_cart(request, product_id):
    product = Menu.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user=request.user
    )
    cart_item.quantity += 1
    cart_item.save()
    return redirect("restr:view_cart")


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect("restr:view_cart")


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            owner = Group.objects.get(name="owner")

            user.groups.add(owner)
            user.save()

            messages.success(
                request, "Account created successfully for " + user.username
            )
            return HttpResponseRedirect(reverse("restr:login"))

    context = {"form": form}

    return render(request, "restr/ownerRegister.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request, username=username, password=password
        )  # matching username and password of login input field and stored usernames from database that is registered

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("restr:index"))

        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, "restr/ownerLogin.html")


def logoutUser(request):
    logout(request)
    return render(request, "restr/ownerLogin.html")


import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View

# from .models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)

        line_items = []

        for item in cart_items:
            line_items.append(
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": item.product.price * 100,
                        "product_data": {
                            "name": item.product.items,
                            "description": "placeholder definition for the product",
                            "images": [
                                "https://5.imimg.com/data5/TestImages/HT/HC/TC/SELLER-89159197/chhole-bhature-paddler-paper-500x500.jpg"
                            ],
                        },
                    },
                    "quantity": item.quantity,
                }
            )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )

        return redirect(checkout_session.url)


from django.views.generic import TemplateView


class SuccessView(TemplateView):
    template_name = "restr/success.html"


class CancelView(TemplateView):
    template_name = "restr/cancel.html"
