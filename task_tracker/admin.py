from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from task_tracker.models import *
# Register your models here.

class TaskAdmin(GuardedModelAdmin):
    pass

class DepartmentAdmin(GuardedModelAdmin):
    pass

class StudentAdmin(GuardedModelAdmin):
    pass
admin.site.register(Task,TaskAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Student,StudentAdmin)