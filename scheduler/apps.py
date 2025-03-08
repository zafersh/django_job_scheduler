from django.apps import AppConfig

class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'
    
    def ready(self):
        # Start background job to do job scheduling
        from .scheduler import JobScheduler
        scheduler = JobScheduler()
        scheduler.start()

