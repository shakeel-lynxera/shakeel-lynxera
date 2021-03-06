# Generated by Django 3.0.4 on 2021-02-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0003_bagger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bagger2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20)),
                ('role', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Bagger',
        ),
    ]