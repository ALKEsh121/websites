from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from onedealsapp.models import *
from django.contrib import messages
from owner.forms import *
from onedealsapp.forms import *
from django.views.generic import UpdateView, DeleteView
from django.views import View
import csv
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail,BadHeaderError
from PIL import Image
import random
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import logging
from django.conf import settings

logger = logging.getLogger(__name__)




# Create your views here.
def is_admin(user):
    return user.is_superuser

@login_required
def dashboard(request):
    visit = Selection.objects.filter(status = "unread").count()
    project= Property.objects.filter(status = 'pending').count()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {
        "enquiry_count":enquiry_count,
        'project':project,
        'visit':visit
        }
    return render(request, "dashboard.html", context)

#services
def ManageService(request):
    services = Services.objects.all()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"services":services, "enquiry_count":enquiry_count}
    return render(request, "manage-services.html", context)



def AddService(request):
    form = AddServiceForm()
    if request.method == 'POST':
        form = AddServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully !!")
            return redirect('manage-services')
    return render(request, "add-service.html", {"form":form})


class UpdateService(UpdateView):
    model = Services
    pk_url_kwarg = "id"
    template_name = "update-service.html"
    success_url = reverse_lazy("manage-services")
    form_class = UpdateServiceForm

    def form_valid(self, form):
        messages.success(self.request, "Service  updated successfully")
        return super().form_valid(form)


class DeleteService(DeleteView):
    model = Services
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-services")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Service deleted successfully")
        return super(DeleteService, self).form_valid(form)


#Projects
def ManageProject(request):
    projects = Property.objects.all()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"projects":projects, "enquiry_count":enquiry_count}
    return render(request, "manage-projects.html", context)


@login_required
def AddProject(request):
    form = AddPropertyForm()
    if request.method == 'POST':
        form = AddPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            land_detail = form.save(commit=False)
            land_detail.user = request.user  # Assign the logged-in user
            if 'image' in request.FILES:
                image = Image.open(request.FILES['image'])
                image = image.resize((800, 500))  # Resize image to 800x600 pixels

                # Save the resized image back to a Django-friendly file object
                image_io = io.BytesIO()
                image.save(image_io, format=image.format)
                image_file = InMemoryUploadedFile(image_io, None, request.FILES['image'].name, 'image/jpeg', image_io.getbuffer().nbytes, None)

                land_detail.image = image_file

            land_detail.save()
            messages.success(request, "Land detail submitted")
            return redirect('manage-projects')
    return render(request, "add-project.html", {"form": form})

@login_required
def land_list(request):
    # Show only approved land details
    land_details = Property.objects.filter(status='approved')
    return render(request, 'land_list.html', {'land_details': land_details})

@user_passes_test(is_admin)
def admin_land_list(request):
    land_details = Property.objects.filter(status='pending')
    return render(request, 'admin_land_list.html', {'land_details': land_details})

@user_passes_test(lambda u: u.is_superuser)

def review_land_detail(request, pk):
    land_detail = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = AdminPropertyForm(request.POST, instance=land_detail)
        if form.is_valid():
            updated_property = form.save(commit=False)
            previous_status = land_detail.status
            updated_property.save()
            
            # Check if the status has changed
            if updated_property.status != previous_status:
                try:
                    if updated_property.status == 'approved':
                        # Prepare the email content for approval
                        subject = 'OneDealsRealty: Property Approved'
                        message = (
                            f"Dear {land_detail.user.username},\n\n"
                            "We are pleased to inform you that your property submission has been approved. "
                            "Your property is now listed and visible to potential buyers.\n\n"
                            "If you have any questions or need further assistance, please do not hesitate to contact us.\n\n"
                            "Best regards,\n"
                            "The OneDealsRealty Team\n"
                            "support@onedealsrealty.in\n"
                            "OneDealsRealty"
                        )
                    else:
                        # Prepare the email content for rejection
                        subject = 'OneDealsRealty: Property Rejected'
                        message = (
                            f"Dear {land_detail.user.username},\n\n"
                            "We regret to inform you that your property submission has been rejected. "
                            "Please review your submission and ensure it meets our guidelines.\n\n"
                            "If you have any questions or need further assistance, please do not hesitate to contact us.\n\n"
                            "Best regards,\n"
                            "The OneDealsRealty Team\n"
                            "support@onedealsrealty.in\n"
                            "OneDealsRealty"
                        )
                    
                    # Log email details
                    logger.info(f"Sending email to {land_detail.user.email} with subject: {subject}")

                    # Send the email
                    send_mail(
                        subject,
                        message,
                        'support@onedealsrealty.in',
                        [land_detail.user.email],
                        fail_silently=False,
                    )

                    # Log success message
                    logger.info(f"Email successfully sent to {land_detail.user.email}")
                    
                    messages.success(request, f"{updated_property.status.capitalize()} email sent to the user!")
                except BadHeaderError:
                    logger.error("Invalid header found.")
                    messages.error(request, "Invalid header found.")
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")
                    messages.error(request, f"An error occurred: {str(e)}")
            else:
                messages.success(request, "Property detail status updated successfully!")
            
            return redirect('admin_land_list')
    else:
        form = AdminPropertyForm(instance=land_detail)
    
    return render(request, 'review_property_detail.html', {'form': form, 'land_detail': land_detail})

class UpdateProject(UpdateView):
    model = Property
    pk_url_kwarg = "id"
    template_name = "update-project.html"
    success_url = reverse_lazy("manage-projects")
    form_class = UpdatePropertyForm

    def form_valid(self, form):
        messages.success(self.request, "Project  updated successfully")
        return super().form_valid(form)


class DeleteProject(DeleteView):
    model = Property
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-projects")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Project deleted successfully")
        return super(DeleteProject, self).form_valid(form)


###################### Enquiry ######################
def ManageEnquiry(request):
    enquiries = Enquiry.objects.all()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"enquiries":enquiries, "enquiry_count":enquiry_count}
    return render(request, "manage-enquiries.html", context)


def ViewEnquiry(request, id):
    enquiry = Enquiry.objects.get(id=id)
    if enquiry.status == "unread":
        enquiry.status = "viewed"
        enquiry.save()
    return render(request, "view-enquiry.html", {"enquiry":enquiry})


class DeleteEnquiry(DeleteView):
    model = Enquiry
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-enquiries")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Enquiry deleted successfully")
        return super(DeleteEnquiry, self).form_valid(form)



############################## subscription ##############################
def ManageSubscribe(request):
    subscription = Subscription.objects.all()
    enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"subscription":subscription, "enquiry_count":enquiry_count}
    return render(request, "manage-subscription.html", context)


class Deletesub(DeleteView):
    model = Subscription
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-subscription")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "subscription deleted successfully")
        return super(Deletesub, self).form_valid(form)




############################## Gallery ########################
def ManageGallery(request):
    gal = Gallery.objects.all()
    # enquiry_count = Enquiry.objects.filter(status="unread").count()
    context = {"proj":gal}
    return render(request, "manage-gallery.html", context)


def AddGallery(request):
    form = AddGalleryForm()
    if request.method == 'POST':
        form = AddGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Images added successfully !!")
            return redirect('manage-gallery')
    return render(request, "add-gallery.html", {"forms":form})


class Updategallery(UpdateView):
    model = Gallery
    pk_url_kwarg = "id"
    template_name = "update-gallery.html"
    success_url = reverse_lazy("manage-gallery")
    form_class = UpdateGalleryForm

    def form_valid(self, form):
        messages.success(self.request, "Gallery  updated successfully")
        return super().form_valid(form)


class Deletegallery(DeleteView):
    model = Gallery
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-gallery")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "image deleted successfully")
        return super(Deletegallery, self).form_valid(form)

################### Download ########################
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






########################## BLOG ############################



def ManageBlog(request):
    blogs = Blog.objects.all()
    context = {"blog":blogs}
    return render(request, 'manage-blog.html',context)


def AddBlog(request):
    form = AddBlogForm()
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "blog added successfully !!")
            return redirect('manage-blog')
    return render(request, "add-blog.html", {"forms":form})


class Updateblog(UpdateView):
    model = Blog
    pk_url_kwarg = "id"
    template_name = "update-blog.html"
    success_url = reverse_lazy("manage-blog")
    form_class = UpdateBlogForm

    def form_valid(self, form):
        messages.success(self.request, "blog  updated successfully")
        return super().form_valid(form)
    

class Deleteblog(DeleteView):
    model = Blog
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-blog")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Blog deleted successfully")
        return super(Deleteblog, self).form_valid(form)
    


##################### Testimonials ###########################


def ManageTestimonials(request):
    testimonial = Testimo.objects.all()
    context = {'testimonial' :testimonial }
    return render (request , 'manage-testimonials.html' , context )

def AddTestimonials(request):
    form = AddTestForm()
    if request.method == 'POST':
        form = AddTestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonials added successfully !!")
            return redirect('manage-testimonial')
    return render(request, "add-testimonials.html", {"form":form})


class UpdateTestimonials(UpdateView):
    model = Testimo
    pk_url_kwarg = "id"
    template_name = "update-testimonials.html"
    success_url = reverse_lazy("manage-testimonials")
    form_class = UpdateTestForm

    def form_valid(self, form):
        messages.success(self.request, "testimonials  updated successfully")
        return super().form_valid(form)
    

class DeleteTestimonials(DeleteView):
    model = Testimo
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-testimonial")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "testimonials deleted successfully")
        return super(DeleteTestimonials, self).form_valid(form)
    

####################################################################################

def UserLogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully !!")
    return redirect('home')


######################################################################################

def ManageVisit(request):
    visits = Selection.objects.all()
    enquiry_count = Selection.objects.filter(status="unread").count()
    context = {"visits":visits, "enquiry_count":enquiry_count}
    return render(request, "manage-visit.html", context)


def ViewVisit(request, id):
    visits = Selection.objects.get(id=id)
    if visits.status == "unread":
        visits.status = "viewed"
        visits.save()
    return render(request, "view-visit.html", {"visits":visits})


class DeleteVisit(DeleteView):
    model = Selection
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-Visit")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Visit deleted successfully")
        return super(DeleteVisit, self).form_valid(form)

##################################################################################


