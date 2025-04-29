from django.urls import path
from .views import *


urlpatterns =[
    path('register/',Register.as_view(),name='register'),
    path('login/',user_login , name='login'),
    
    #jobseeker dashboard #
    path('jobseeker/',jobseekerhomepage,name = 'jobseeker'),
    path('apply/<int:pk>/',jobseeker_applicationpage,name='apply'),
    path('applications',all_applied,name='applications'),

    #employer dashboard 
    path('employer/',employer,name='employer'),
    path('view_application/<int:pk>/',ViewApplication,name ='View application'),
    path('delete_application/<int:pk>/',delete_application,name ='Delete application'),
    path('create_vacancies/',CreateVacancies,name='create')
    ]