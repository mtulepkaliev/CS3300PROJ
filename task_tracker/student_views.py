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

class studentDetailView(generic.DetailView):
    model = Student

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
            student.save()

            messages.success(request,'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request,'registration/register.html',context)
