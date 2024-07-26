from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SuperUserRegistrationForm(forms.ModelForm):
    is_superuser = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_superuser')

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)


class SelectionForm(forms.Form):
    # Define choices for dropdowns
    STATES = [
        ('', 'Select State'),
        ('KL', 'Keralam'),
        ('TN', 'Tamil Nadu'),
        ('KA', 'Karanadaka'),
        ('MP','Madhya Pradesh'),
        ('MH','Maharashtra'),
        ('MN','Manipur'),
        ('AR','Arunachal Pradesh'),
        ('AS','Assam'),
        ('BR','Bihar'),
        ('CG','Chhattisgarh '),
        ('GA','Goa'),
        ('GJ','Gujarat'),
        ('HR','Haryana'),
        ('HP','Himachal Pradesh'),
        ('JK','Jammu and Kashmir'),
        ('JH','Jharkhand '),
        ('RJ','Rajasthan'),
        ('SK','Sikkim'),
        ('PB','Punjab'),
        ('OR','Orissa'),
        ('NL','Nagaland'),
        ('UP','Uttar Pradesh '),



        # Add more states as needed
    ]


    COUNTRIES = [
        ('IN', 'India'),

        # Add more countries as needed
    ]


    TRANSACTION_TYPES = [
        ('', 'Select Transaction Type'),
        ('sale', 'Sale'),
        ('rent', 'Rent'),
        ('lease', 'Lease'),
    ]

    PROPERTY_PREFERENCES = [
        ('', 'Select Property Preference'),
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('land', 'Land'),
    ]

    NUM_BATHROOMS = [
        ('', 'Select Number of Bathrooms'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4 or more'),
    ]

    NUM_BEDROOMS = [
        ('', 'Select Number of Bedrooms'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4 or more'),
    ]

    PREFERRED_AMENITIES = [
        ('pool', 'Pool'),
        ('gym', 'Gym'),
        ('parking', 'Parking'),
        ('garden', 'Garden'),
        ('security', 'Security'),
        # Add more amenities as needed
    ]

    CONTACT_METHODS = [
        ('', 'Select Preferred Contact Method'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('text', 'Text'),
    ]

    HOW_DID_YOU_HEAR_ABOUT_US = [
        ('', 'How Did You Hear About Us?'),
        ('friend', 'Friend/Family'),
        ('online_ad', 'Online Ad'),
        ('social_media', 'Social Media'),
        ('search_engine', 'Search Engine'),
        ('other', 'Other'),
    ]
    CITY = [
        ('', 'Select city'),
        ('14','Kazarkode'),
        ('13','Kannur'),
        ('12','wayanadu'),
        ('11','Kozhikode'),
        ('10','Malappuram'),
        ('09','Palakkad'),
        ('08','Thrissur'),
        ('07','Ernakulam'),
        ('06','Idukki'),
        ('05','Alappuzha'),
        ('04','Kottayam'),
        ('03','Pathanamthitta'),
        ('02','Kollam'),
        ('01','Thiruvananthapuram'),

    ]

    # Define form fields
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Phone', max_length=15, required=True)
    address_line_1 = forms.CharField(label='Address Line 1', max_length=255, required=True)
    address_line_2 = forms.CharField(label='Address Line 2', max_length=255, required=False)
    city = forms.ChoiceField(label='City',choices=CITY, required=True)
    state = forms.ChoiceField(label='State', choices=STATES, required=True)
    postal_code = forms.CharField(label='Postal Code', max_length=10, required=True)
    country = forms.ChoiceField(label='Country', choices=COUNTRIES, required=True)
    transaction_type = forms.ChoiceField(label='Type of Transaction', choices=TRANSACTION_TYPES, required=True)
    property_preference = forms.ChoiceField(label='Property Preference', choices=PROPERTY_PREFERENCES, required=True)
    num_bathrooms = forms.ChoiceField(label='Number of Bathrooms', choices=NUM_BATHROOMS, required=False)
    num_bedrooms = forms.ChoiceField(label='Number of Bedrooms', choices=NUM_BEDROOMS, required=False)
    
    # New fields
    preferred_amenities = forms.MultipleChoiceField(
        label='Preferred Amenities (if applicable)',
        choices=PREFERRED_AMENITIES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    budget = forms.DecimalField(
        label='Budget',
        max_digits=10,
        decimal_places=2,
        required=True,
        help_text='Enter your budget (e.g., 150000.00)'
    )
    preferred_contact_method = forms.ChoiceField(
        label='Preferred Contact Method',
        choices=CONTACT_METHODS,
        required=True
    )
    how_did_you_hear_about_us = forms.ChoiceField(
        label='How Did You Hear About Us?',
        choices=HOW_DID_YOU_HEAR_ABOUT_US,
        required=True
    )
    additional_comments = forms.CharField(
        label='Additional Comments/Requirements',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    privacy_policy = forms.BooleanField(
        label='I agree to the Privacy Policy',
        required=True
    )






