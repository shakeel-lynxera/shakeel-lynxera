# Generated by Django 3.1.3 on 2021-02-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seller', '0002_delete_addtocart'),
    ]

    operations = [
        migrations.CreateModel(
            name='seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
                ('address', models.TextField()),
            ],
        ),
    ]
