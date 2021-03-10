from authModule import models
from django.contrib import admin
from .models import ResetPassword, Seller, ShopHour, UserRole,UserProfile, Driver, License, Vehicle

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserRole)
admin.site.register(ResetPassword)
admin.site.register(Driver)
admin.site.register(License)
admin.site.register(Vehicle)
admin.site.register(Seller)
admin.site.register(ShopHour)