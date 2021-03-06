from django.db import models


class LogEntryForException(models.Model):
    url = models.TextField(default='', db_column='url')
    user_agent = models.TextField(default='', db_column='user_agent')
    ip_address = models.TextField(default='', db_column='ip_address')
    exception = models.TextField(null=False, db_column='exception')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'LogEntryForException'


class Role(models.Model):
    name = models.CharField(max_length=32, db_column='name')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'Role'
