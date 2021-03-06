# Generated by Django 3.1 on 2021-03-06 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntryForException',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(db_column='url', default='')),
                ('user_agent', models.TextField(db_column='user_agent', default='')),
                ('ip_address', models.TextField(db_column='ip_address', default='')),
                ('exception', models.TextField(db_column='exception')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
            ],
            options={
                'db_table': 'LogEntryForException',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
            ],
            options={
                'db_table': 'Role',
            },
        ),
    ]
