# Generated by Django 5.0 on 2023-12-26 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]