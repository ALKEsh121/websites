from django.shortcuts import render,redirect,get_object_or_404
import requests
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from onedealsapp.models import *
from django.contrib import messages
from userapp.forms import *
from django.views.generic import UpdateView, DeleteView
from django.views import View
import csv
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from PIL import Image
import random
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
@login_required
def UserHome(request):
    Project = Property.objects.all()
    project_reject = Property.objects.filter(status = 'rejected').count()
    project_uncount = Property.objects.filter(status = "pending").count()
    project_count = Property.objects.filter(status="approved").count()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    
    

    api_key = '5b834c0ddad9299ee1f9363782830bd6'
    # city = request.GET.get('kochi')  # Default to New York if city parameter is not provided
    city = "trivandrum"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    response = requests.get(url)
    data = response.json()
    print(data)

    weather_data = {
        'city': data['name'],
        'country': data['sys']['country'],
        'temperature': data['main']['temp'],
    }
    
    context = {
        'Project':Project,
        'weather':weather_data,
        "enquiry_count":enquiry_count,
        "project_count":project_count,
        'project_uncount':project_uncount,
        'project_reject':project_reject
        }
   
    return render(request,'home.html',context)



@login_required
def ManageServices(request):
    services = Services.objects.all()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"services":services, "enquiry_count":enquiry_count}
    return render(request, "manageservices.html", context)


@login_required
def AddServices(request):
    form = AddServiceForms()
    if request.method == 'POST':
        form = AddServiceForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully !!")
            return redirect('manage-services')
    return render(request, "addservice.html", {"form":form})


class UpdateServices(UpdateView):
    model = Services
    pk_url_kwarg = "id"
    template_name = "update-service.html"
    success_url = reverse_lazy("manage-services")
    form_class = UpdateServiceForms

    def form_valid(self, form):
        messages.success(self.request, "Service  updated successfully")
        return super().form_valid(form)


class DeleteServices(DeleteView):
    model = Services
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-services")
    template_name = "confirmdelete.html"

    def form_valid(self, form):
        messages.success(self.request, "Service deleted successfully")
        return super(DeleteServices, self).form_valid(form)


###################################### PROJECT #############################################

@login_required
def ManageProject(request):
    projects = Property.objects.all()
    project_count = Property.objects.filter(status="approved").count()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"projects":projects, "enquiry_count":enquiry_count,"project_count":project_count}
    return render(request, "manageprojects.html", context)


@login_required
def AddProject(request):
    form = AddPropertyForms()
    if request.method == 'POST':
        form = AddPropertyForms(request.POST, request.FILES)
        if form.is_valid():
            land_detail = form.save(commit=False)
            land_detail.user = request.user  # Assign the logged-in user

            # Resize the image
            if 'image' in request.FILES:
                image = Image.open(request.FILES['image'])
                image = image.resize((800, 600))  # Resize image to 800x600 pixels

                # Save the resized image back to a Django-friendly file object
                image_format = image.format if image.format else 'JPEG'
                image_io = io.BytesIO()
                image.save(image_io, format=image_format)
                image_file = InMemoryUploadedFile(image_io, None, request.FILES['image'].name, f'image/{image_format.lower()}', image_io.getbuffer().nbytes, None)

                land_detail.image = image_file

            land_detail.save()

            subject = 'OneDealsRealty: Property Submission Received'
            message = (
                f"Dear {request.user.username},\n\n"
                "Thank you for submitting your property details to OneDealsRealty. Your property is currently under review.\n\n"
                "We will notify you once the review process is completed.\n\n"
                "Best regards,\n"
                "The OneDealsRealty Team\n"
                "support@onedealsrealty.in\n"
                "OneDealsRealty"
            )
            send_mail(
                subject,
                message,
                'support@onedealsrealty.in',
                [request.user.email],
                fail_silently=False
            )

            messages.success(request, "Land detail submitted for review!")
            return redirect('manage-project')
    return render(request, "addproject.html", {"form": form})


class UpdateProjects(UpdateView):
    model = Property
    pk_url_kwarg = "id"
    template_name = "update-project.html"
    success_url = reverse_lazy("manage-project")
    form_class = UpdatePropertyForms

    def form_valid(self, form):
        messages.success(self.request, "Property  updated successfully")
        return super().form_valid(form)


class DeleteProjects(DeleteView):
    model = Property
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-project")
    template_name = "confirmdelete.html"

    def form_valid(self, form):
        messages.success(self.request, "Property deleted successfully")
        return super(DeleteProjects, self).form_valid(form)
    




################################## ENQUIRY #########################################

@login_required
def ManageEnquirys(request):
    enquiries = Enquiry.objects.all()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"enquiries":enquiries, "enquiry_count":enquiry_count}
    return render(request, "manageenquiries.html", context)


def ViewEnquirys(request, id):
    enquiry = Enquiry.objects.get(id=id)
    if enquiry.status == "unread":
        enquiry.status = "viewed"
        enquiry.save()
    return render(request, "viewenquiry.html", {"enquiry":enquiry})


class DeleteEnquirys(DeleteView):
    model = Enquiry
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-enquiries")
    template_name = "confirmdelete.html"

    def form_valid(self, form):
        messages.success(self.request, "Enquiry deleted successfully")
        return super(DeleteEnquirys, self).form_valid(form)
    
def ManagePending(request):
    return render(request,"manage-pending.html")
    


################################## Download #################################
class DownloadDataView(View):
    def get(self, request):
        data = Enquiry.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
        writer = csv.writer(response)
        writer.writerow(['name','email','phone','message'])
        for row in data:
            writer.writerow([row.name,row.email,row.phone,row.message])


        return response




def UserLogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully !!")
    return redirect('home')