from typing import Text
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, TextField
from django.utils import tree
from utilities.models import Role
from authModule.models import *
from django.utils.timezone import datetime


class Vendor(models.Model):
    full_name = TextField(default='', db_column='full_name')
    email_address = TextField(default='', db_column='email_address')
    phone_number = TextField(default='', db_column='phone_number')
    company = TextField(default='', db_column='company')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    shop = models.ForeignKey(Shop, null=True,on_delete=models.CASCADE, db_column='shop')


class Shop_Product(models.Model):
    title = models.TextField(default='', db_column='title')
    description = models.TextField(default='', db_column='description')
    price = models.IntegerField(default=0, db_column='price')
    sale_price = models.IntegerField(default=0, db_column='sale_price')
    is_active = models.BooleanField(default=False, db_column='is_active')
    sku = models.TextField(default='', db_column='sku')
    barcode = models.TextField(default='', db_column='barcode')
    quantity = models.IntegerField(default=0, db_column='quantity')
    weight = models.FloatField(default='', db_column='weight')
    weight_unit = models.TextField(default='', db_column='weight_unit')
    tags = models.TextField(default='', db_column='tags')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column='vendor')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, db_column='seller')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='shop')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')


class Shop_Product_Category(models.Model):
    name = TextField(default='', db_column='name')
    shop_product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE, db_column='shop_product')

class Shop_Product_Type(models.Model):
    name = TextField(default='', db_column='name')
    shop_product_category = models.ForeignKey(Shop_Product_Category, on_delete=models.CASCADE, db_column='shop_product_category')

class Shop_Product_Variant(models.Model):
    name = models.TextField(default='', db_column='name')
    value = models.TextField(default='', db_column='value')
    price = models.IntegerField(default=0, db_column='price')
    sale_price = models.IntegerField(default=0, db_column='sale_price')
    sku = models.TextField(default='', db_column='sku')
    barcode = models.TextField(default='', db_column='barcode')
    quantity = models.IntegerField(default=0, db_column='quantity')
    shop_product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE,  db_column='shop_product')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')