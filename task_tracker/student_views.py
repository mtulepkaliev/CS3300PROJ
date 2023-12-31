from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

class studentDetailView(generic.DetailView):
    model = Student
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['student_department_list'] = context['object'].getMembership()
        if(self.request.user.is_authenticated and self.request.user.has_perm('task_tracker.manage_student',context['object'])):
            context['can_edit'] = True
        return context

#view for the register page
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
            student.first_name = form.cleaned_data['first_name']
            student.last_name = form.cleaned_data['last_name']
            student.save()
            student.updateMembership(form.cleaned_data['departments'])

            messages.success(request,'Account was created for ' + username)
            return redirect('login')
        else:
            print(form.errors)
            print("form is invalid")
            messages.error(request,'Form is invalid')
            context = {'form':form} 
            return render(request,'registration/register.html',context)

    context = {'form':form}
    return render(request,'registration/register.html',context)

@login_required(login_url='login')
def studentDeleteView(request,**kwargs):
    student = Student.objects.get(id=kwargs['pk'])
    if(request.user.has_perm('task_tracker.manage_student',student)):
        if request.method == 'POST':
            student.user.delete()
            student.delete()
            return redirect('login')
        else:
            return render(request,'task_tracker/student_confirm_delete.html',{'student':student})
    else:
        return HttpResponse("You do not have permission to delete this student")

@login_required(login_url='login')
def studentUpdateView(request,**kwargs):
    student = Student.objects.get(id=kwargs['pk'])
    if( request.user.has_perm('task_tracker.manage_student',student)):
        if request.method == 'POST':
            form = UpdateStudentForm(request.POST,instance=student)
            if form.is_valid():
                departmentMembership = form.cleaned_data['departments']
                student.updateMembership(departmentMembership)
                form.save()
                return redirect('student-detail-view',pk=kwargs['pk'])
        else:
            form = UpdateStudentForm(instance=student)
            #https://stackoverflow.com/questions/26966527/django-modelmultiplechoicefield-set-initial-values
            form.fields['departments'].initial = student.getMembership()
        return render(request,'task_tracker/student_update_form.html',{'form':form})
    else:
        return HttpResponse("You do not have permission to edit this student")



            

            