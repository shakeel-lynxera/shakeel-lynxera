from django.db import models
from django.contrib.auth.models import User
from utilities.models import Role


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    name = models.TextField(default='', db_column='name')

    class Meta:
        db_table = 'UserProfile'


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'UserRole'
