from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('workflow/', views.workflow, name='workflow'),
    path('join/', views.join, name='join'),
    path('order/', views.order, name='order'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('applications/', views.applications, name='applications'),
    path('register/', views.register, name='register'),
    path('applications/<int:request_id>/', views.request_detail, name='request_detail'),
]