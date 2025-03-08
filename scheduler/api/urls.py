from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .dashboard_stats import dashboard_stats

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('submit-job/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/status/', views.job_status, name='job_status'),
    path('user/jobs/', views.user_jobs, name='user_jobs'),
    path('dashboard-stats/', dashboard_stats, name='dashboard_stats'),
]

