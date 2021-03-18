from authModule import models
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Shop_Product_Type)
admin.site.register(Shop_Product_Variant)
admin.site.register(Shop_Product_Category)
admin.site.register(Shop_Product)