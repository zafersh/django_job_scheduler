from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Job(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    estimated_duration = models.PositiveIntegerField(help_text="Duration in seconds")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def wait_time(self):
        """Calculate the wait time in seconds"""
        if self.started_at:
            return (self.started_at - self.created_at).total_seconds()
        return (timezone.now() - self.created_at).total_seconds()
    
    @property
    def execution_time(self):
        """Calculate the execution time in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        if self.started_at:
            return (timezone.now() - self.started_at).total_seconds()
        return 0
    
    @property
    def time_to_deadline(self):
        """Calculate time remaining until deadline in seconds"""
        return (self.deadline - timezone.now()).total_seconds()
    
    @property
    def is_overdue(self):
        """Check if job is overdue"""
        return timezone.now() > self.deadline

