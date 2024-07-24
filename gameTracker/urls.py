"""
URL configuration for gameTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gtApp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('userReg', views.userReg),
    path('login', views.login),



    path('adminHome', views.adminHome),
    path('adminUsers', views.adminUsers),
    path('adminApproveUser', views.adminApproveUser),
    path('adminDeleteUser', views.adminDeleteUser),
    path('adminBlogs', views.adminBlogs),
    path('adminDeleteBlog', views.adminDeleteBlog),
    path('adminViewBlogs', views.adminViewBlogs),


    path('userHome', views.userHome),
    path('userGames', views.userGames),
    path('userViewGame', views.userViewGame),
    path('userProgress', views.userProgress),
    path('userBlogs', views.userBlogs),
    path('userViewBlogs', views.userViewBlogs),
    path('userViewUsers', views.userViewUsers),
    path('userVideos', views.userVideos),
    path('userDeleteVideo', views.userDeleteVideo),
    path('userViewVideos', views.userViewVideos),
    path('userDeletProgress', views.userDeletProgress),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= "reset_password.html"),name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name= "reset_password_done.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]
