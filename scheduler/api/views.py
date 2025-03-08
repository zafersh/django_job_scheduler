from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from scheduler.models import Job
from .serializers import JobSerializer
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit their jobs.
    
    list:
    Returns a list of all jobs for the current user.
    
    create:
    Create a new job.
    
    retrieve:
    Return the given job if it belongs to the current user.
    
    update:
    Update the given job if it belongs to the current user.
    
    partial_update:
    Partially update the given job if it belongs to the current user.
    
    destroy:
    Delete the given job if it belongs to the current user.
    """
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only return jobs for the current user
        return Job.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def job_status(request, job_id):
    """
    API endpoint to get only the status of a specific job.
    
    Returns:
    {
        "id": job_id,
        "status": "pending|running|completed|failed"
    }
    """
    try:
        job = Job.objects.get(id=job_id, user=request.user)
        return Response({
            "id": job.id,
            "status": job.status
        })
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_jobs(request):
    """
    API endpoint to get all jobs for the current user.
    
    Optional query parameters:
    - status: Filter jobs by status (pending, running, completed, failed)
    - priority: Filter jobs by priority (high, medium, low)
    
    Returns:
    List of jobs belonging to the current user.
    """
    jobs = Job.objects.filter(user=request.user)
    
    # Filter by status if provided
    status_filter = request.query_params.get('status')
    if status_filter and status_filter in dict(Job.STATUS_CHOICES).keys():
        jobs = jobs.filter(status=status_filter)
    
    # Filter by priority if provided
    priority_filter = request.query_params.get('priority')
    if priority_filter and priority_filter in dict(Job.PRIORITY_CHOICES).keys():
        jobs = jobs.filter(priority=priority_filter)
    
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_job(request):
    try:
        data = json.loads(request.body)
        name = data['name']
        user = request.user
        estimated_duration = data['estimated_duration']
        priority = data['priority']
        deadline = data['deadline']

        job = Job.objects.create(
            name=name,
            user=user,
            estimated_duration=estimated_duration,
            priority=priority,
            deadline=deadline,
            created_at=timezone.now()
        )

        return Response({'status': 'success', 'job_id': job.id})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)})
