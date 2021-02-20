from django.db import models
from django.db.models.fields import CharField


class mUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.username