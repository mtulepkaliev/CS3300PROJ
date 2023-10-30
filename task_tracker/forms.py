from django.forms import ModelForm
import django.forms as forms
from .models import Task
from django.contrib.admin.widgets import AdminDateWidget



class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['summary','detail','deadline','priority','department','parent_task']
        #override dealdine to use a date picker
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

        #custom labels for the form
        labels = {
            'summary': 'Summary',
            'detail': 'Detail',
            'deadline': 'Deadline (Optional)',
            'priority': 'Priority',
            'department': 'Department',
            'parent_task': 'Parent Task (Optional)',
        }