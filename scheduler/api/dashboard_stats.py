from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from scheduler.models import Job

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """API endpoint to get dashboard statistics"""
    user_jobs = Job.objects.filter(user=request.user)
    
    # Count jobs by status
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
    
    # Count jobs by priority
    priority_counts = {
        'high': user_jobs.filter(priority='high').count(),
        'medium': user_jobs.filter(priority='medium').count(),
        'low': user_jobs.filter(priority='low').count(),
    }
    
    return Response({
        'pending_jobs': pending_jobs,
        'running_jobs': running_jobs,
        'completed_jobs': completed_jobs,
        'failed_jobs': failed_jobs,
        'avg_wait_time': avg_wait_time,
        'priority_counts': priority_counts,
    })

