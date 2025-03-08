from rest_framework import serializers
from scheduler.models import Job

class JobSerializer(serializers.ModelSerializer):
    wait_time = serializers.SerializerMethodField()
    execution_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'name', 'estimated_duration', 'priority', 
            'deadline', 'status', 'created_at', 'started_at', 
            'completed_at', 'wait_time', 'execution_time'
        ]
        read_only_fields = ['id', 'created_at', 'started_at', 'completed_at', 'status']
    
    def get_wait_time(self, obj):
        return obj.wait_time
    
    def get_execution_time(self, obj):
        return obj.execution_time
    
    def create(self, validated_data):
        # Set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

