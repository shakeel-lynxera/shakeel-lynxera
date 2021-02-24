from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField


class mUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, default="null-mail")
    phone = models.BigIntegerField(default=12345)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length = 20, choices = (
                                                        (1, 'Driver'),
                                                        (2, 'Seller'),
                                                        (3, 'Buyer')
                                                        ))

class mUserRegistration(models.Model):
    email = models.CharField(max_length=50, default='')
    verification_code = models.CharField(max_length=6, default='')

    def __str__(self):
        return self.email