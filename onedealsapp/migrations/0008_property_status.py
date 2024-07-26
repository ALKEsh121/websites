# Generated by Django 5.0.6 on 2024-07-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedealsapp', '0007_remove_property_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
