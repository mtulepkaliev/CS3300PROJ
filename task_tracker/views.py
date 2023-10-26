from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):

# Render the HTML template index.html with the data in the context variable.
   return render(request,'task_tracker/base_template.html')
