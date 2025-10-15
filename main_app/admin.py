from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass
from .models import Cars, Requests

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'status')

@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'car_id', 'status')