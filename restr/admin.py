from django.contrib import admin
from .models import Menu
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

admin.site.register(Menu)
