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
            return Task.objects.filter(departments=self.kwargs['department_id']).order_by('is_complete','deadline','priority')

class taskDetailView(generic.DetailView):
    model = Task
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context['object'].departments.all)
        return super().get_context_data(**kwargs)

class departmentDetailView(generic.DetailView):
    model = Department

class studentDetailView(generic.DetailView):
    model = Student

@login_required(login_url='login')
def taskCreateView(request,**kwargs):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-list-view')
    else:
        form = TaskForm()
    return render(request,'task_tracker/task_form.html',{'form':form})

@login_required(login_url='login')
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

@login_required(login_url='login')
def taskDeleteView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    if request.method == 'POST':
        task.delete()
        return redirect('task-list-view')
    else:
        return render(request,'task_tracker/task_confirm_delete.html',{'task':task})

@login_required(login_url='login')
def taskToggleCompleteView(request,**kwargs):
    task = Task.objects.get(id=kwargs['pk'])
    task.is_complete = not task.is_complete
    task.save()
    #redirect to the page that made the request, makes the change seamless
    return redirect(request.META['HTTP_REFERER'])

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

def registerPage(request):

    form = CreateStudentForm()
    if(request.method == 'POST'):
        #make a createstudent form
        form = CreateStudentForm(request.POST)
        if(form.is_valid()):
            #fill out a user form with the fields
            userForm = CreateUserForm(request.POST)
            username = form.cleaned_data['username']
            userForm.username = username
            userForm.email = form.cleaned_data['email']
            userForm.password1 = form.cleaned_data['password1']
            userForm.password2 = form.cleaned_data['password2']
            print("user form filled out")
            #print(messages.get_messages(request))
            if(userForm.is_valid()):
                #save the user
                print("user form is valid")
                user = userForm.save()
            else:
                print(userForm.errors)
                print("user form is invalid")
                messages.error(request,'User form is invalid')
                form.errors.update(userForm.errors)
                context = {'form':form}
                return render(request,'registration/register.html',context)
            #add the user to the students group
            studentGroup = Group.objects.get(name='student')
            user.groups.add(studentGroup)
            student = Student.objects.create(user=user)
            student.save()

            messages.success(request,'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request,'registration/register.html',context)
