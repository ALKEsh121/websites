from django.urls import path
from . import views

urlpatterns  = [
    path('',views.UserHome,name = 'userhome'),
        ###################### service manager ##########################
    path('manage-service', views.ManageServices, name="manage-service"),
    path("add-services",views.AddServices, name="add-services"),
    path("update-services/<int:id>/",views.UpdateServices.as_view(), name="update-services"),
    path("delete-services/<int:id>/",views.DeleteServices.as_view(), name="delete-services"),

    ###################### project manager ##########################
    path('manage-project', views.ManageProject, name="manage-project"),
    path("add-projects",views.AddProject, name="add-projects"),
    path("update-projects/<int:id>/",views.UpdateProjects.as_view(), name="update-projects"),
    path("delete-projects/<int:id>/",views.DeleteProjects.as_view(), name="delete-projects"),
    
    
    
    ###################### Enquiry manager ##########################
    path('manage-enquirie', views.ManageEnquirys, name="manage-enquirie"),
    path("view-enquirys/<int:id>/",views.ViewEnquirys, name="view-enquirys"),
    path("delete-enquirys/<int:id>/",views.DeleteEnquirys.as_view(), name="delete-enquirys"),

    ####################### Pending Manager ##########################
    path('manage-pending', views.ManagePending, name="manage-pending"),




    path('download-data/', views.DownloadDataView.as_view(), name='download_data'),
    path('logout',views.UserLogout,name='logout')


]