
from django.contrib import admin
from django.urls import path,include
from accounts import views

urlpatterns = [
    
    path('login/', views.login_page, name='login'),
    path('', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_user, name='logout'),


    path('blogs/', views.blogsall, name='blogs'),
    path('drafts/', views.drafts, name='drafts'),
    path('myblog/', views.myblogs, name='myblogs'),
    path('create/', views.createBlog, name='create'),
    path('mhealth/', views.mhealth, name='mhealth'),
    path('heartdis/', views.heartdis, name='heartdis'),
    path('covid19/', views.covid19, name='covid19'),
    path('immun/', views.immun, name='immun'),
]
