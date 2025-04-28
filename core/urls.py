from django.urls import path
from .views import *


urlpatterns =[
    path('register/',Register.as_view(),name='register'),
    path('',home,name='homepage'),
    path('login/',user_login , name='login'),
    
    #jobseeker dashboard #
    path('jobseeker/',jobseekerhomepage,name = 'jobseeker'),
    path('apply/<int:pk>/',jobseeker_applicationpage,name='apply'),

    #employer dashboard 
    path('employerdashboard/',employer,name='employer')
    ]