# Generated by Django 5.0.6 on 2024-07-11 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedealsapp', '0008_property_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]