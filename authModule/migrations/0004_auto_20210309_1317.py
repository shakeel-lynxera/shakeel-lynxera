# Generated by Django 3.0.4 on 2021-03-09 08:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0003_auto_20210309_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpassword',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
