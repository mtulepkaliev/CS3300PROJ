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
   return render(request, 'task_tracker/index.html')

class taskListView(generic.ListView):
    model = Task
    template_name = 'task_tracker/task_list.html'

    #puts all the completed tasks at the bottom and orders the rest by deadline
    def get_queryset(self):

        #print out only that department's tasks if department_id is in the url
        if('department_id' not in self.kwargs):
            return Task.objects.all().order_by('is_complete','deadline','priority')
        else:
            return Task.objects.filter(department=self.kwargs['department_id']).order_by('is_complete','deadline','priority')

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
    return render(request,'task_tracker/task_form.html',{'form':form})

def taskUpdateView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-detail-view',pk=kwargs['pk'])
    else:
        form = TaskForm(instance=task)
    return render(request,'task_tracker/task_form.html',{'form':form})

def taskDeleteView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    if request.method == 'POST':
        task.delete()
        return redirect('task-list-view')
    else:
        return render(request,'task_tracker/task_confirm_delete.html',{'task':task})

def taskToggleCompleteView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    task.is_complete = not task.is_complete
    task.save()
    #redirect to the page that made the request, makes the change seamless
    return redirect(request.META['HTTP_REFERER'])

