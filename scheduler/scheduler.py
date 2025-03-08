import time
import threading
import logging
from datetime import datetime
from django.utils import timezone
from .models import Job

logger = logging.getLogger(__name__)

class JobScheduler:
    """
    Job scheduler that implements a priority-based algorithm with deadline consideration.
    It uses a combination of priority levels and Earliest Deadline First (EDF) algorithm.
    """
    
    def __init__(self):
        # Max 3 job run together
        self.max_concurrent_jobs = 3 
        self.running = False
        self.scheduler_thread = None
    
    def start(self):
        """Start the scheduler in a separate thread"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            logger.info("Job scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
            logger.info("Job scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            try:
                running_jobs_count = Job.objects.filter(status='running').count()
                # Make sure that only 3 job are allowed to run simultaneously.
                if running_jobs_count < self.max_concurrent_jobs:
                    # Get the next job to run based on our scheduling algorithm
                    next_job = self._get_next_job()
                    
                    if next_job:
                        # Start the job in a separate thread
                        self._start_job(next_job)
                
                # Sleep for a short time before checking again
                time.sleep(1)
            
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)  # Sleep longer on error
    
    def _get_next_job(self):
        """
        Get the next job to run based on priority and deadline.
        
        Algorithm:
        1. First, try to get high priority jobs ordered by deadline
        2. If no high priority jobs, try medium priority jobs ordered by deadline
        3. If no medium priority jobs, try low priority jobs ordered by deadline
        """
        pending_jobs = Job.objects.filter(status='pending')
        
        if not pending_jobs.exists():
            return None
        
        # Try to get jobs by priority level, ordered by deadline
        for priority in ['high', 'medium', 'low']:
            jobs = pending_jobs.filter(priority=priority).order_by('deadline')
            if jobs.exists():
                return jobs.first()
        
        return None
    
    def _start_job(self, job):
        """Start a job and update its status"""
        try:
            # Update job status to running and set start time
            job.status = 'running'
            job.started_at = timezone.now()
            job.save()
            
            # Start job execution in a separate thread
            job_thread = threading.Thread(target=self._execute_job, args=(job,))
            job_thread.daemon = True
            job_thread.start()
            
            logger.info(f"Started job: {job.name} (ID: {job.id})")
        
        except Exception as e:
            logger.error(f"Error starting job {job.id}: {e}")
            job.status = 'failed'
            job.save()
    
    def _execute_job(self, job):
        """Execute a job (simulate work with sleep)"""
        try:
            # Simulate job execution
            time.sleep(job.estimated_duration)
            
            # Update job status to completed
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            
            logger.info(f"Completed job: {job.name} (ID: {job.id})")
        
        except Exception as e:
            logger.error(f"Error executing job {job.id}: {e}")
            job.status = 'failed'
            job.save()

