from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):

    #TODO remove this as we will be implementing department model later
    department_choices = [("All","ALL"),("EE","Electrical"), ("MECH","Mechanical"),("BUS","Business")]
    
    priority_choices = [(3,"LOW"),(2,"MEDIUM"),(1,"HIGH")]

    summary = models.CharField(max_length=200)
    detail = models.TextField(max_length=1000)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=priority_choices,default=3,null=False,blank=False)
    parent_task = models.ForeignKey('self',related_name="children",on_delete=models.CASCADE,blank=True,null=True)

    #TODO change to FK
    department = models.CharField(max_length=200,choices=department_choices,default="All",blank=False)

    def __str__(self):
        return self.summary
    
    # https://stackoverflow.com/questions/59698423/when-should-you-use-property-in-a-model-class
    @property
    def is_overdue(self):
        if(self.deadline and self.deadline < timezone.now()):
            return True
        else:
            return False

    # Recursively collect children, used to figure out what would get removed with cascade delete  
    # https://stackoverflow.com/questions/35281293/recursively-collect-children-in-python-django
    @property
    def child_tasks(self):
        childTasks = self.children.all()
        if not childTasks:
            return None
        else:
            for task in childTasks:
                if task.child_tasks:
                    childTasks = childTasks | task.child_tasks
            return childTasks