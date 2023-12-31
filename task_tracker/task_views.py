from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


class taskListView(generic.ListView):
    model = Task
    template_name = 'task_tracker/task_list.html'

    #puts all the completed tasks at the bottom and orders the rest by deadline
    def get_queryset(self):

        #print out only that department's tasks if department_id is in the url
        if('department_id' not in self.kwargs):
            return Task.objects.all().order_by('is_complete','deadline','priority')
        else:
            return Task.objects.filter(departments=self.kwargs['department_id']).order_by('is_complete','deadline','priority')
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if('department_id' in self.kwargs):
            context['department'] = Department.objects.get(id=self.kwargs['department_id'])
        return context

class taskDetailView(generic.DetailView):
    model = Task
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        thisTask = context['object']
        if(self.request.user.is_authenticated and self.request.user.has_perm('task_tracker.manage_task',thisTask)):
            context['can_edit'] = True
        return context
    
@login_required(login_url='login')
def taskCreateView(request,**kwargs):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            task = form.instance
            task.updatePermissions(task.departments.all(),task.assignedStudents.all())
            return redirect('task-list-view')
    else:
        form = TaskForm()
    return render(request,'task_tracker/task_form.html',{'form':form})

@login_required(login_url='login')
def taskUpdateView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    #check user permissions
    if request.user.has_perm('task_tracker.manage_task',task):
        if request.method == 'POST':
            form = TaskForm(request.POST,instance=task)
            if form.is_valid():
                form.save()
                task = form.instance
                task.updatePermissions(task.departments.all(),task.assignedStudents.all())
                return redirect('task-detail-view',pk=kwargs['pk'])
        else:
            form = TaskForm(instance=task)
            return render(request,'task_tracker/task_form.html',{'form':form})
    else:
        return HttpResponse("You do not have permission to edit this task")
   

@login_required(login_url='login')
def taskDeleteView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    if request.user.has_perm('task_tracker.manage_task',task):
        if request.method == 'POST':
            task.delete()
            return redirect('task-list-view')
        else:
            return render(request,'task_tracker/task_confirm_delete.html',{'task':task})
    else:
        return HttpResponse("You do not have permission to delete this task")
    
@login_required(login_url='login')
def taskToggleCompleteView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    #only change status if the user has permissions for that task
    if request.user.has_perm('task_tracker.manage_task',task):
        task.is_complete = not task.is_complete
        task.save()
    #redirect to the page that made the request, makes the change seamless
    return redirect(request.META['HTTP_REFERER'])