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

class departmentDetailView(generic.DetailView):
    model = Department


class departmentListView(generic.ListView):
    model = Department
    template_name = 'task_tracker/department_list.html'
    context_object_name = 'department_list'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['wtf_department_solution_list'] = Department.objects.all()
        print(context['wtf_department_solution_list'])
        return context
    
@login_required(login_url='login')
def departmentCreateView(request,**kwargs):
    if request.method == 'POST':
        form = CreateDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-list-view')
    else:
        form = CreateDepartmentForm()
    return render(request,'task_tracker/department_form.html',{'form':form})

@login_required(login_url='login')
def departmentUpdateView(request,**kwargs):
    department = Department.objects.get(id=kwargs['pk'])
    if request.method == 'POST':
        form = CreateDepartmentForm(request.POST,instance=department)
        if form.is_valid():
            form.save()
            return redirect('department-detail-view',pk=kwargs['pk'])
    else:
        form = CreateDepartmentForm(instance=department)
    return render(request,'task_tracker/department_form.html',{'form':form})

@login_required(login_url='login')
def departmentDeleteView(request,**kwargs):
    department = Department.objects.get(id=kwargs['pk'])
    if request.method == 'POST':
        department.delete()
        return redirect('department-list-view')
    else:
        return render(request,'task_tracker/department_confirm_delete.html',{'department':department})
