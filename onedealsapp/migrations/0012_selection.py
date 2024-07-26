# Generated by Django 5.0.6 on 2024-07-15 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onedealsapp', '0011_services_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('', 'Select State'), ('KL', 'Keralam'), ('TN', 'Tamil Nadu'), ('KA', 'Karanadaka'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chhattisgarh '), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand '), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('PB', 'Punjab'), ('OR', 'Orissa'), ('NL', 'Nagaland'), ('UP', 'Uttar Pradesh ')], max_length=2)),
                ('postal_code', models.CharField(max_length=10)),
                ('country', models.CharField(choices=[('IN', 'India')], max_length=2)),
                ('transaction_type', models.CharField(choices=[('', 'Select Transaction Type'), ('sale', 'Sale'), ('rent', 'Rent'), ('lease', 'Lease')], max_length=10)),
                ('property_preference', models.CharField(choices=[('', 'Select Property Preference'), ('house', 'House'), ('apartment', 'Apartment'), ('condo', 'Condo'), ('land', 'Land')], max_length=20)),
                ('num_bathrooms', models.CharField(blank=True, choices=[('', 'Select Number of Bathrooms'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4 or more')], max_length=1, null=True)),
                ('num_bedrooms', models.CharField(blank=True, choices=[('', 'Select Number of Bedrooms'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4 or more')], max_length=1, null=True)),
                ('preferred_amenities', models.CharField(blank=True, max_length=20, null=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('preferred_contact_method', models.CharField(choices=[('', 'Select Preferred Contact Method'), ('email', 'Email'), ('phone', 'Phone'), ('text', 'Text')], max_length=10)),
                ('how_did_you_hear_about_us', models.CharField(choices=[('', 'How Did You Hear About Us?'), ('friend', 'Friend/Family'), ('online_ad', 'Online Ad'), ('social_media', 'Social Media'), ('search_engine', 'Search Engine'), ('other', 'Other')], max_length=20)),
                ('additional_comments', models.TextField(blank=True, null=True)),
                ('privacy_policy', models.BooleanField()),
            ],
        ),
    ]
