from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from task_tracker.models import *
# Register your models here.

class TaskAdmin(GuardedModelAdmin):
    pass
admin.site.register(Task,TaskAdmin)
admin.site.register(Department)
admin.site.register(Student)