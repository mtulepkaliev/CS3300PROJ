from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.utils import timezone
from.forms import TaskForm  

# Create your views here.
def index(request):

# Render the HTML template index.html with the data in the context variable.
   return redirect('task-list-view')

class taskListView(generic.ListView):
    model = Task

    #puts all the completed tasks at the bottom and orders the rest by deadline
    def get_queryset(self):
        return Task.objects.all().order_by('is_complete','deadline','priority')

class taskDetailView(generic.DetailView):
    model = Task

def taskCreateView(request,**kwargs):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-list-view')
    else:
        form = TaskForm()
    return render(request,'task_tracker/create_task_form.html',{'form':form})


