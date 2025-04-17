from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('join/', views.join, name='join'),
    path('order/', views.order, name='order'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('applications/', views.applications, name='applications'),
    path('applications/<int:request_id>/', views.request_detail, name='request_detail'),
    path('applications/designer/<int:pk>/', views.designer_application_detail, name='designer_application_detail'),
    path('delete-request/<int:pk>/', views.delete_request, name='delete_request'),
    path('workflow/', views.workflow, name='workflow'),
    path('workflow/delete/<int:pk>/', views.delete_stage, name='delete_stage'),
    path('workflow/add/', views.add_stage, name='add_stage'),
    path('workflow/update/<int:pk>/', views.update_stage, name='update_stage'),



]