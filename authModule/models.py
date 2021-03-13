from typing import Text
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, TextField
from django.utils import tree
from utilities.models import Role
from django.utils.timezone import datetime
# from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    name = models.TextField(default='', db_column='name')
    address = models.TextField(default='', db_column='address')
    phone_number = models.TextField(default='', db_column='phone_number')
    date_of_birth = models.CharField(default='', max_length=15 ,db_column='date_of_birth')
    is_seller = BooleanField(default=False, db_column='is_seller')
    is_buyer = BooleanField(default=False, db_column='is_buyer')
    is_driver = BooleanField(default=False, db_column='is_driver')
    
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'UserProfile'


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'UserRole'

class ResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False ,db_column='user')
    verification_code = models.CharField(default='', max_length=6, db_column='verification_code')
    key_expires = models.DateTimeField(default=datetime.now, db_column='key_expires')

    class Meta:
        db_table = 'ResetPassword'

    def __str__(self):
        return self.verification_code

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='user')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, db_column='profile')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=False, db_column='role')
    social_security_number = models.TextField(default='', db_column='social_security_number')

    class Meta:
        db_table = 'Driver'

class License(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True ,db_column='driver')
    license_state = models.TextField(default='', db_column='license_state')
    license_number = models.TextField(default='', db_column='license_number')
    license_exp_date = models.TextField(default='', db_column='license_exp_date')

class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True ,db_column='driver')
    vehicle_type = models.TextField(default='', db_column='vehicle_type')
    vehicle_make = models.TextField(default='', db_column='vehicle_make')
    vehicle_number = models.TextField(default='', db_column='vehicle_number')
    vehicle_color = models.TextField(default='', db_column='vehicle_color')

    class Meta:
        db_table = 'Vehicle'

class Bank_card_detail(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True ,db_column='driver')
    name_of_card = CharField(default='', max_length=30, db_column='name_of_card')
    card_number = CharField(default='', max_length=30, db_column='card_number')
    expiry_date = CharField(default='', max_length=30, db_column='expiry_date')
    cvv_number = CharField(default='', max_length=3, db_column='cvv_number')
    billing_address = TextField(default='', db_column='billing_address')
    is_save = BooleanField(default=False, db_column='is_save')

    class Meta:
        db_table = 'Bank_card_details'




class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=False, db_column='profile')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=False, db_column='role')

    class Meta:
        db_table = 'Seller'


class Shop(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False, db_column='seller')
    shop_name = models.TextField(default='', db_column='shop_name')
    shop_address = models.TextField(default='', db_column='shop_address')
    open_time = models.TextField(default='', db_column='open_time')
    close_time = models.TextField(default='', db_column='close_time')
    is_always_open = models.BooleanField(default=False, db_column='is_always_open')
    # week = JSONField()
    # day = models.TextField(default='', db_column='day')
    # open_time = models.TextField(default='', db_column='open_time')
    # close_time = models.TextField(default='', db_column='close_time')
    # is_24hours_open = models.BooleanField(default=False, db_column='is_24hours_open')

    class Meta:
        db_table = 'ShopHour'