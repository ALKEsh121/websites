# Generated by Django 5.0.6 on 2024-07-24 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onedealsapp', '0020_rename_description_testimo_caption_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testimo',
            old_name='photo',
            new_name='image',
        ),
    ]