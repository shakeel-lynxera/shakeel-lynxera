# Generated by Django 3.0.4 on 2021-03-11 13:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_state', models.TextField(db_column='license_state', default='')),
                ('license_number', models.TextField(db_column='license_number', default='')),
                ('license_exp_date', models.TextField(db_column='license_exp_date', default='')),
            ],
        ),
        migrations.CreateModel(
            name='ShopHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_time', models.TextField(db_column='open_time', default='')),
                ('close_time', models.TextField(db_column='close_time', default='')),
                ('is_always_open', models.BooleanField(db_column='is_always_open', default=False)),
            ],
            options={
                'db_table': 'ShopHour',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.TextField(db_column='vehicle_type', default='')),
                ('vehicle_make', models.TextField(db_column='vehicle_make', default='')),
                ('vehicle_number', models.TextField(db_column='vehicle_number', default='')),
                ('vehicle_color', models.TextField(db_column='vehicle_color', default='')),
            ],
            options={
                'db_table': 'Vehicle',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('role', models.ForeignKey(db_column='role', on_delete=django.db.models.deletion.CASCADE, to='utilities.Role')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserRole',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_column='name', default='')),
                ('address', models.TextField(db_column='address', default='')),
                ('is_set_password', models.BooleanField(db_column='is_set_password', default=False)),
                ('phone_number', models.TextField(db_column='phone_number', default='')),
                ('date_of_birth', models.CharField(db_column='date_of_birth', default='', max_length=15)),
                ('user', models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserProfile',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(db_column='profile', on_delete=django.db.models.deletion.CASCADE, to='authModule.UserProfile')),
                ('role', models.OneToOneField(db_column='role', on_delete=django.db.models.deletion.CASCADE, to='authModule.UserRole')),
                ('shopHour', models.OneToOneField(db_column='shopHour', on_delete=django.db.models.deletion.CASCADE, to='authModule.ShopHour')),
                ('user', models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Seller',
            },
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_code', models.CharField(db_column='verification_code', default='', max_length=6)),
                ('key_expires', models.DateTimeField(db_column='key_expires', default=datetime.datetime.now)),
                ('user', models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ResetPassword',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_security_number', models.TextField(db_column='social_security_number', default='')),
                ('license', models.OneToOneField(db_column='license', on_delete=django.db.models.deletion.CASCADE, to='authModule.License')),
                ('profile', models.OneToOneField(db_column='profile', on_delete=django.db.models.deletion.CASCADE, to='authModule.UserProfile')),
                ('role', models.OneToOneField(db_column='role', on_delete=django.db.models.deletion.CASCADE, to='authModule.UserRole')),
                ('user', models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.OneToOneField(db_column='vehicle', on_delete=django.db.models.deletion.CASCADE, to='authModule.Vehicle')),
            ],
            options={
                'db_table': 'Driver',
            },
        ),
    ]
