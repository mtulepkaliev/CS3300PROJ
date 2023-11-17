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
