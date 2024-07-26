from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
import random
from django.core.mail import send_mail
from django.views.decorators.http import require_POST




def send_otp(user):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    OTP.objects.update_or_create(user=user, defaults={'otp': otp})
    
    subject = 'OneDealsRealty: Your OTP Verification Code'
    message = (
        f"Dear {user.username},\n\n"
        "Thank you for choosing OneDealsRealty, a leading provider of tailored real estate marketing solutions. We specialize in crafting customized marketing strategies to showcase properties effectively and drive successful transactions for property owners, developers, and investors.\n\n"
        "To complete your registration or login process, please use the following OTP (One-Time Password) code:\n\n"
        f"Your OTP Code: {otp}\n\n"
        "This code is valid for a short period. Please enter it on the verification page to proceed.\n\n"
        "At OneDealsRealty, we are committed to delivering exceptional service and client satisfaction. Should you have any questions or need further assistance, feel free to contact us.\n\n"
        "Best regards,\n"
        "The OneDealsRealty Team\n"
        "support@onedealsrealty.in\n"
        "OneDealsRealty"
    )
    
    send_mail(
        subject,
        message,
        'support@onedealsrealty.in',
        [user.email],
        fail_silently=False,
    )


# def register(request):
#     if request.method == 'POST':
#         form = SuperUserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             if form.cleaned_data['is_superuser']:
#                 user.is_superuser = True
#                 user.is_staff = True
#                 user.save()
#                 login(request, user)
#                 return redirect('home')
#             send_otp(user)
#             return redirect('verify_otp')
#     else:
#         form = SuperUserRegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def RegisterPage(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             if user.is_superuser:
#                 login(request, user)
#                 return redirect('home')
#             send_otp(user)
#             messages.success(request, "User created successfully.")
#             return redirect("verify_otp")
#         else:
#             return render(request, "registerpage.html", {'form':form})
#     return render(request, "registerpage.html", {'form':form})



# def verify_otp(request):
#     user = request.user
#     if user.is_authenticated:
#         # Check if OTP has been verified already
#         if request.session.get('otp_verified', False):
#             return redirect('home')

#         if user.is_superuser:
#             login(request, user)
#             return redirect('home')

#     if request.method == 'POST':
#         if 'resend_otp' in request.POST:
#             send_otp(user)
#             messages.success(request, 'OTP has been resent to your email.')
#             return redirect('verify_otp')

#         form = OTPForm(request.POST)
#         if form.is_valid():
#             otp = form.cleaned_data['otp']
#             otp_record = OTP.objects.filter(otp=otp).first()
#             if otp_record and otp_record.is_valid():
#                 user = otp_record.user
#                 login(request, user)

#                 request.session['otp_verified'] = True


#                 subject = 'OneDealsRealty: Email Verification Successful'
#                 message = (
#                     f"Dear {user.username},\n\n"
#                     "We are pleased to inform you that your email has been successfully verified. "
#                     "You can now enjoy the full benefits of our real estate services.\n\n"
#                     "At OneDealsRealty, we strive to provide exceptional service and support to our clients. "
#                     "If you have any questions or need further assistance, please do not hesitate to contact us.\n\n"
#                     "Best regards,\n"
#                     "The OneDealsRealty Team\n"
#                     "support@onedealsrealty.in\n"
#                     "OneDealsRealty"
#                 )
                
#                 send_mail(
#                     subject,
#                     message,
#                     'support@onedealsrealty.in',
#                     [user.email],
#                     fail_silently=False
#                 )
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid OTP')
#     else:
#         form = OTPForm()
#     return render(request, 'verify_otp.html', {'form': form})



# def LoginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_superuser:
#                 login(request, user)
#                 return redirect('home')
#             if not request.session.get('otp_verified', False):
#                 send_otp(user)
#                 messages.success(request, "OTP sent to your email. Please verify.")
#                 return redirect('verify_otp')
#             else:
#                 login(request, user)
#                 return redirect('home')
#         else:
#             messages.info(request, "Invalid Login Credentials")
#             return redirect("login")
#     return render(request, "loginpage.html")

def register(request):
    if request.method == 'POST':
        form = SuperUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['is_superuser']:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                login(request, user)
                return redirect('home')
            send_otp(user)
            return redirect('verify_otp')
    else:
        form = SuperUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_superuser:
                login(request, user)
                return redirect('home')
            send_otp(user)
            messages.success(request, "User created successfully.")
            return redirect("verify_otp")
        else:
            return render(request, "registerpage.html", {'form': form})
    return render(request, "registerpage.html", {'form': form})


def verify_otp(request):
    user = request.user
    if user.is_authenticated:
        # Check if OTP has been verified already
        if request.session.get('otp_verified', False):
            return redirect('home')

        if user.is_superuser:
            login(request, user)
            return redirect('home')

    if request.method == 'POST':
        if 'resend_otp' in request.POST:
            send_otp(user)
            messages.success(request, 'OTP has been resent to your email.')
            return redirect('verify_otp')

        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            otp_record = OTP.objects.filter(otp=otp).first()
            if otp_record and otp_record.is_valid():
                user = otp_record.user
                login(request, user)

                request.session['otp_verified'] = True

                subject = 'OneDealsRealty: Email Verification Successful'
                message = (
                    f"Dear {user.username},\n\n"
                    "We are pleased to inform you that your email has been successfully verified. "
                    "You can now enjoy the full benefits of our real estate services.\n\n"
                    "At OneDealsRealty, we strive to provide exceptional service and support to our clients. "
                    "If you have any questions or need further assistance, please do not hesitate to contact us.\n\n"
                    "Best regards,\n"
                    "The OneDealsRealty Team\n"
                    "support@onedealsrealty.in\n"
                    "OneDealsRealty"
                )

                send_mail(
                    subject,
                    message,
                    'support@onedealsrealty.in',
                    [user.email],
                    fail_silently=False
                )
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('home')
            if request.session.get('otp_verified', True):
                login(request, user)
                return redirect('home')
                
            else:
                send_otp(user)
                messages.success(request, "OTP sent to your email. Please verify.")
                return redirect('verify_otp')
        else:
            messages.info(request, "Invalid Login Credentials")
            return redirect("login")
    return render(request, "loginpage.html")



#Logout
def UserLogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully !!")
    return redirect('home')



def home(request):
    services = Services.objects.all()
    testimonials= Testimo.objects.all()
    projects = Property.objects.filter(status='approved')
    context = {
        "services":services, 
        "projects":projects,
        "testimonials":testimonials
        }
    return render(request, "index.html", context)


def About(request):
    return render(request, "about.html")


def service(request):
    services = Services.objects.all()
    context = {"services":services}
    return render(request, "service.html", context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        pro_id = request.POST.get('id')
        Enquiry.objects.create(name=name, email=email, phone=phone, message=message,pro_id=pro_id)  
        messages.success(request, "Thank you for contacting us !!!")
        return redirect("home")
    return render(request, "contact.html")


def property(request):
    projects = Property.objects.filter(status='approved')
    context = {"projects":projects}
    return render(request, "properties.html", context)

def PorjectDetails(request,id):
    projects =get_object_or_404(Property, id=id, status='approved')
    testimonials = Testimo.objects.all()
    context = {
        "projects":projects,
        "testimonials":testimonials
        }
    return render(request,"property-details.html",context)




#Subscription
def subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        Subscription.objects.create(email=email)
        messages.success(request, "Thank you for subscribing !!!")
        return redirect('/')

@login_required
def ProjectDetail(request, id):
    project = Property.objects.get(id=id)
    context = {"project":project}
    return render(request, "project-details.html", context)

@login_required
def ServiceDetail(request, id):
    service = Services.objects.get(id=id)
    context = {"service":service}
    return render(request, "service-details.html", context)

def selection(request):
    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            postal_code = form.cleaned_data['postal_code']
            country = form.cleaned_data['country']
            transaction_type = form.cleaned_data['transaction_type']
            property_preference = form.cleaned_data['property_preference']
            num_bathrooms = form.cleaned_data['num_bathrooms']
            num_bedrooms = form.cleaned_data['num_bedrooms']
            preferred_amenities = form.cleaned_data['preferred_amenities']
            budget = form.cleaned_data['budget']
            preferred_contact_method = form.cleaned_data['preferred_contact_method']
            how_did_you_hear_about_us = form.cleaned_data['how_did_you_hear_about_us']
            additional_comments = form.cleaned_data['additional_comments']
            privacy_policy = form.cleaned_data['privacy_policy']

            inquiry = Selection(
                name=name,
                email=email,
                phone=phone,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                transaction_type=transaction_type,
                property_preference=property_preference,
                num_bathrooms=num_bathrooms,
                num_bedrooms=num_bedrooms,
                preferred_amenities=preferred_amenities,
                budget=budget,
                preferred_contact_method=preferred_contact_method,
                how_did_you_hear_about_us=how_did_you_hear_about_us,
                additional_comments=additional_comments,
                privacy_policy=privacy_policy
            )
            inquiry.save()
            messages.success(request, "Thank you for contacting us, our Agents will contact you soon !!!")
            return redirect('home')  # Redirect or render a success page
            
    else:
        form = SelectionForm()

    return render(request, 'selection.html', {'form': form})