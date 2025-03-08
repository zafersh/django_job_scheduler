from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/submit/', views.submit_job, name='submit_job'),
]

