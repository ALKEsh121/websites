# Generated by Django 5.0.6 on 2024-07-24 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedealsapp', '0017_alter_property_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='custom_id',
            field=models.CharField(default=0, max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='property',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
