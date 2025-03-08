from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Job

class JobForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now() + timedelta(hours=1)
    )
    
    class Meta:
        model = Job
        fields = ['name', 'estimated_duration', 'priority', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline

