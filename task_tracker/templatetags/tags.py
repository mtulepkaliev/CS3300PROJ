#https://stackoverflow.com/questions/21062560/django-variable-in-base-html

from django import template
from task_tracker.models import Department

register = template.Library()

@register.simple_tag
def department_name_id_dict(request):
    return Department.objects.all().values('name','id')