from django import forms
from django.forms import ModelForm
from onedealsapp.models import *


#service
class AddServiceForms(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class UpdateServiceForms(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


#projects
class AddPropertyForms(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name','caption','location','image','price','bedrooms','bathrooms','area','floor','parking','description']


class UpdatePropertyForms(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name','caption','location','image','price','bedrooms','bathrooms','area','floor','parking','description']


