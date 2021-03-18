from django.db import models


class LogEntryForException(models.Model):
    url = models.TextField(default='', db_column='url')
    user_agent = models.TextField(default='', db_column='user_agent')
    ip_address = models.TextField(default='', db_column='ip_address')
    exception = models.TextField(null=False, db_column='exception')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    def __str__(self):
        return self.exception

    class Meta:
        db_table = 'LogEntryForException'


class Role(models.Model):
    name = models.CharField(max_length=32, db_column='name')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Role'


class Temp_Product_Barcode_Scanner(models.Model):
    barcode = models.TextField(default='', db_column='barcode')
    title = models.TextField(default='', db_column='title')
    product_img = models.TextField(default='', db_column='product_img')
    category = models.TextField(default='category', db_column='category')
    type = models.TextField(default='', db_column='type')