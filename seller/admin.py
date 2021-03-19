from authModule import models
from django.contrib import admin
from .models import *




class VendorAttributes(admin.ModelAdmin):
    list_display = ('id','full_name', 'email_address', 'phone_number', 'company', 'shop')

class ProductAttributes(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'is_active', 'sku', 'barcode','quantity','weight','weight_unit','tags','vendor','seller','shop')

class ProductTypeAttributes(admin.ModelAdmin):
    list_display = ('id','name', 'shop_product_category')

class ProductCategoryAttributes(admin.ModelAdmin):
    list_display = ('id','name', 'shop_product')

class ProductVariantAttributes(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'sale_price', 'sku', 'barcode','quantity','shop_product')


# Register your models here.
admin.site.register(Vendor, VendorAttributes)
admin.site.register(Shop_Product_Type, ProductTypeAttributes)
admin.site.register(Shop_Product_Variant, ProductVariantAttributes)
admin.site.register(Shop_Product_Category, ProductCategoryAttributes)
admin.site.register(Shop_Product, ProductAttributes)