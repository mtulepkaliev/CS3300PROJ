from django.db import models

# Create your models here.
class Task(models.Model):

    #TODO remove this as we will be implementing department model later
    department_choices = [("All","ALL"),("EE","Electrical"), ("MECH","Mechanical"),("BUS","Business")]

    summary = models.CharField(max_length=200)
    detail = models.TextField(max_length=1000)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    #TODO change to FK
    department = models.CharField(max_length=200,choices=department_choices,default="All",blank=False)

    def __str__(self):
        return self.summary