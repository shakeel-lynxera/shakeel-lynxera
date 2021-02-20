from django.db import models

# Create your models here.


class seller(models.Model):
    name = models.TextField()
    phone = models.TextField()
    email = models.TextField()
    address = models.TextField()
