from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Avg, Count, Q, F
from django.utils import timezone
from .models import Job
from .forms import JobForm
from rest_framework.decorators import api_view

def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
  else:
    if request.user.is_authenticated:
      return redirect('dashboard')
    
    form = AuthenticationForm()
  
  return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_jobs = Job.objects.filter(user=request.user)
    
    # Analytics
    pending_jobs = user_jobs.filter(status='pending').count()
    running_jobs = user_jobs.filter(status='running').count()
    completed_jobs = user_jobs.filter(status='completed').count()
    failed_jobs = user_jobs.filter(status='failed').count()
    
    # Calculate average wait time manually (SQLite compatible)
    jobs_with_start = user_jobs.filter(started_at__isnull=False)
    if jobs_with_start.exists():
        total_wait_time = sum(job.wait_time for job in jobs_with_start)
        avg_wait_time = total_wait_time / jobs_with_start.count()
    else:
        avg_wait_time = 0
    
    priority_counts = {
        'high': user_jobs.filter(priority='high').count(),
        'medium': user_jobs.filter(priority='medium').count(),
        'low': user_jobs.filter(priority='low').count(),
    }
    
    context = {
        'pending_jobs': pending_jobs,
        'running_jobs': running_jobs,
        'completed_jobs': completed_jobs,
        'failed_jobs': failed_jobs,
        'avg_wait_time': avg_wait_time,
        'priority_counts': priority_counts,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def job_list(request):
    user_jobs = Job.objects.filter(user=request.user)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter and status_filter in dict(Job.STATUS_CHOICES).keys():
        user_jobs = user_jobs.filter(status=status_filter)
    
    context = {
        'jobs': user_jobs,
    }
    
    return render(request, 'job_list.html', context)

@login_required
def submit_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    
    return render(request, 'submit_job.html', {'form': form})

