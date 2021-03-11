from django.db import models
from django.contrib.auth.models import User
from utilities.models import Role
from django.utils.timezone import datetime
# from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    name = models.TextField(default='', db_column='name')
    address = models.TextField(default='', db_column='address')
    is_set_password = models.BooleanField(default=False, db_column='is_set_password')
    phone_number = models.TextField(default='', db_column='phone_number')
    date_of_birth = models.CharField(default='', max_length=15 ,db_column='date_of_birth')
    
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

class License(models.Model):
    license_state = models.TextField(default='', db_column='license_state')
    license_number = models.TextField(default='', db_column='license_number')
    license_exp_date = models.TextField(default='', db_column='license_exp_date')

class Vehicle(models.Model):
    vehicle_type = models.TextField(default='', db_column='vehicle_type')
    vehicle_make = models.TextField(default='', db_column='vehicle_make')
    vehicle_number = models.TextField(default='', db_column='vehicle_number')
    vehicle_color = models.TextField(default='', db_column='vehicle_color')

    class Meta:
        db_table = 'Vehicle'


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=False, db_column='profile')
    role = models.OneToOneField(UserRole, on_delete=models.CASCADE, null=False, db_column='role')
    license = models.OneToOneField(License, on_delete=models.CASCADE, null=False, db_column='license')
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=False, db_column='vehicle')
    social_security_number = models.TextField(default='', db_column='social_security_number')

    class Meta:
        db_table = 'Driver'


class ShopHour(models.Model):
    open_time = models.TextField(default='', db_column='open_time')
    close_time = models.TextField(default='', db_column='close_time')
    is_always_open = models.BooleanField(default=False, db_column='is_always_open')

    class Meta:
        db_table = 'ShopHour'
    # week = JSONField()
    # day = models.TextField(default='', db_column='day')
    # open_time = models.TextField(default='', db_column='open_time')
    # close_time = models.TextField(default='', db_column='close_time')
    # is_24hours_open = models.BooleanField(default=False, db_column='is_24hours_open')



class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=False, db_column='profile')
    role = models.OneToOneField(UserRole, on_delete=models.CASCADE, null=False, db_column='role')
    shopHour = models.OneToOneField(ShopHour, on_delete=models.CASCADE, null=False, db_column='shopHour')

    class Meta:
        db_table = 'Seller'