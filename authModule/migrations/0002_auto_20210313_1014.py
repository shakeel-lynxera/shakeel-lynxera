# Generated by Django 3.0.4 on 2021-03-13 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shophour',
            name='shop_address',
            field=models.TextField(db_column='shop_address', default=''),
        ),
        migrations.AddField(
            model_name='shophour',
            name='shop_name',
            field=models.TextField(db_column='shop_name', default=''),
        ),
    ]
