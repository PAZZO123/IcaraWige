from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create/', views.create, name='create'),
    path('update/<str:pk>/', views.updater, name='update'),
    path('delete/<str:pk>/', views.deleter, name='delete'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('deletem/<str:pk>/', views.deletem, name='deletem'),
    path('profile/<str:pk>/', views.userp, name='profile'),
    path('updateu/', views.updateUser, name='updateu'),
    path('topic/', views.topicPage, name='topic'),
    path('activity/', views.activityPage, name='activity'),
    path('', views.landingPage, name='land'),
    path('about/', views.aboutUs, name='about'),
    path('contact/', views.contactUs, name='contact'),
]