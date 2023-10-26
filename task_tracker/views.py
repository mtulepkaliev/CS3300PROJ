from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import *
# Create your views here.
def index(request):

# Render the HTML template index.html with the data in the context variable.
   return render(request,'task_tracker/base_template.html')

class taskListView(generic.ListView):
   model = Task
