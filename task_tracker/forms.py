from django.forms import ModelForm
import django.forms as forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['summary','detail','deadline','priority','departments','parent_task','assignedStudents']
        #override dealdine to use a date picker
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'departments': forms.CheckboxSelectMultiple(),
        }

        #custom labels for the form
        labels = {
            'summary': 'Summary',
            'detail': 'Detail',
            'deadline': 'Deadline (Optional)',
            'priority': 'Priority',
            'departments': 'Department',
            'parent_task': 'Parent Task (Optional)',
            'assignedStudents': 'Assigned Students (Optional)',
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CreateStudentForm(ModelForm):
    #form fields to be passed to the user form
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=200,widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput())

    departments = forms.ModelMultipleChoiceField(queryset=Department.objects.all(),widget=forms.CheckboxSelectMultiple())

    
    class Meta:
        model = Student
        fields = ['first_name',"last_name"]

class UpdateStudentForm(ModelForm):
    departments = forms.ModelMultipleChoiceField(queryset=Department.objects.all(),widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Student
        fields = ['first_name',"last_name"]

class CreateDepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name','description']