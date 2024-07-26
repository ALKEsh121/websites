from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import *
from . forms import SelectionForm
import uuid


class Property(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    custom_id = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/project')
    price = models.IntegerField()
    bedrooms = models.CharField(max_length=100)
    bathrooms = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    floor = models.IntegerField()
    parking = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def save(self, *args, **kwargs):
        if not self.custom_id:
            # Generate unique custom ID
            self.custom_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        # Generate a unique alphanumeric ID
        return str(uuid.uuid4())[:8].replace('-', '').upper()

    def __str__(self):
        return f"{self.custom_id} - {self.name}" 

    def __str__(self):
        return f"Land Detail by {self.user.username} - {self.location}"


class Services(models.Model):
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()

    def __str__(self):
        return self.caption

class Contact(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    pro_id = models.CharField(max_length=20)
    options = (
        ("unread", "unread"),
        ("viewed", "viewed")
    )
    status = models.CharField(max_length=15, choices=options, default="unread")

    def __str__(self):
        return self.name

class Subscription(models.Model):
    email = models.EmailField(null=True)

class Enquiry(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    pro_id = models.CharField(max_length=20)

    options = (
        ("unread", "unread"),
        ("viewed", "viewed")
    )
    status = models.CharField(max_length=15, choices=options, default="unread")

    def __str__(self):
        return self.name  # Adjust based on what identifies the enquiry

class Blog(models.Model):
    image = models.ImageField(upload_to='gallery/blog')
    images = models.ImageField(upload_to='gallery/blog', null=True)
    blogersphoto = models.ImageField(upload_to='gallery/bloguser')
    description = models.CharField(max_length=200)
    details = models.TextField()
    detailsof = models.TextField()
    name = models.CharField(max_length=20)
    caption = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    blogersquote = models.TextField()

    def __str__(self):
        return self.name

class Testimo(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='gallery/testimonials', null=True)
    caption = models.TextField(max_length=300)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    caption = models.CharField(max_length=50)
    description = models.CharField(max_length=40)
    images = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.caption



class UserUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()  # Example field for uploaded data
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Upload by {self.user.username} - Approved: {self.is_approved}"
    
class Selection(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=2,choices=SelectionForm.CITY)
    state = models.CharField(max_length=2, choices=SelectionForm.STATES)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=2, choices=SelectionForm.COUNTRIES)
    transaction_type = models.CharField(max_length=10, choices=SelectionForm.TRANSACTION_TYPES)
    property_preference = models.CharField(max_length=20, choices=SelectionForm.PROPERTY_PREFERENCES)
    num_bathrooms = models.CharField(max_length=1, choices=SelectionForm.NUM_BATHROOMS, blank=True, null=True)
    num_bedrooms = models.CharField(max_length=1, choices=SelectionForm.NUM_BEDROOMS, blank=True, null=True)
    preferred_amenities = models.CharField(max_length=20, blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_contact_method = models.CharField(max_length=10, choices=SelectionForm.CONTACT_METHODS)
    how_did_you_hear_about_us = models.CharField(max_length=20, choices=SelectionForm.HOW_DID_YOU_HEAR_ABOUT_US)
    additional_comments = models.TextField(blank=True, null=True)
    privacy_policy = models.BooleanField()
    options = (
        ("unread", "unread"),
        ("viewed", "viewed")
    )
    status = models.CharField(max_length=15, choices=options, default="unread")

    def __str__(self):
        return self.name
    


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def is_valid(self):
        now = datetime.now(timezone.utc)
        return now - self.created_at < timedelta(minutes=5)