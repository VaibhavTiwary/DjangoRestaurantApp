from django.contrib import admin
from .models import Menu, CartItem
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

admin.site.register(Menu)
admin.site.register(CartItem)
