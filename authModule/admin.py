from seller.admin import ProductTypeAttributes
from authModule import models
from django.contrib import admin
from .models import *

# Register your models here.


class ProfileAttributes(admin.ModelAdmin):
    list_display = ('user', 'name', 'address', 'lat', 'lng', 'phone_number','date_of_birth', 'is_seller', 'is_buyer', 'is_driver')

class UserRoleAttributes(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active')

class ResetPasswordAttributes(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'key_expires')

class DriverAttributes(admin.ModelAdmin):
    list_display = ('user', 'profile', 'role', 'social_security_number', 'lat', 'lng')

class LicenseAttributes(admin.ModelAdmin):
    list_display = ('driver', 'license_state', 'license_number','license_exp_date')

class VehicleAttributes(admin.ModelAdmin):
    list_display = ('driver', 'vehicle_type', 'vehicle_make', 'vehicle_number', 'vehicle_color')

class BankAttributes(admin.ModelAdmin):
    list_display = ('driver', 'name_of_card', 'card_number', 'expiry_date', 'cvv_number', 'billing_address', 'is_save')

class SellerAttributes(admin.ModelAdmin):
    list_display = ('user', 'profile', 'role')

class ShopsAttributes(admin.ModelAdmin):
    list_display = ('seller', 'shop_name', 'shop_address', 'open_time', 'close_time', 'is_always_open', 'lat', 'lng')




admin.site.register(UserProfile, ProfileAttributes)
admin.site.register(UserRole, UserRoleAttributes)
admin.site.register(ResetPassword, ResetPasswordAttributes)
admin.site.register(Driver, DriverAttributes)
admin.site.register(License, LicenseAttributes)
admin.site.register(Vehicle, VehicleAttributes)
admin.site.register(Seller, SellerAttributes)
admin.site.register(Shop, ShopsAttributes)