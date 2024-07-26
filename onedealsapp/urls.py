from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.LoginPage, name = 'login'),
    path('logout',views.UserLogout, name = 'logout'),
    path('contact', views.contact, name="contact"),
    path('register', views.RegisterPage, name="register"),
    path('property', views.property, name="property"),
    path('selection', views.selection, name="selection"),
    path('service', views.service, name="service"),
    path('service-details/<int:id>/', views.ServiceDetail, name="service-details"),

    path('about', views.About, name="about"),
    path('project-details/<int:id>/', views.PorjectDetails, name="project-details"),







    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.verify_otp, name='resend_otp'),



    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='forgot_password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_complete.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


]