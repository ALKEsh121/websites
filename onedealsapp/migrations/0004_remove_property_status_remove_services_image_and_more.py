# Generated by Django 5.0.6 on 2024-07-10 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onedealsapp', '0003_property_area_property_bathrooms_property_bedrooms_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='status',
        ),
        migrations.RemoveField(
            model_name='services',
            name='image',
        ),
        migrations.RemoveField(
            model_name='services',
            name='name',
        ),
        migrations.RemoveField(
            model_name='services',
            name='price',
        ),
    ]