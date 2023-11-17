from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User,Group
from guardian.shortcuts import assign_perm,get_perms,remove_perm

# Create your models here.
class Task(models.Model):

    
    priority_choices = [(3,"LOW"),(2,"MEDIUM"),(1,"HIGH")]

    summary = models.CharField(max_length=200)
    detail = models.TextField(max_length=1000)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=priority_choices,default=3,null=False,blank=False)
    parent_task = models.ForeignKey('self',related_name="children",on_delete=models.CASCADE,blank=True,null=True)

    #M:N relationship with Department
    departments = models.ManyToManyField('Department',related_name="tasks",blank=True)

    #M;N relationship with Student
    assignedStudents = models.ManyToManyField('Student',related_name="assignedTasks",blank=True)

    class Meta:
        permissions = (
            ('manage_task','Manage task'),
        )

    def save(self, *args, **kwargs):
        #if the task is being created, not updated
        if(not self.pk):
            #give the admin group permission to manage the task
            adminGroup = Group.objects.get(name='admin')
            assign_perm('manage_task',adminGroup,self)
        
        self.updatePermissions(self.departments.all(),self.assignedStudents.all())

        #propogate department permissions to children
        if self.child_tasks:
            for child in self.child_tasks:
                
                #if the child is not in the same departments as the parent, add the parent's departments to the child
                for department in self.departments.all():
                    if not department in child.departments.all():
                        child.departments.add(department)
                
                #add the department permissions to the child
                child.updatePermissions(self.departments.all(),child.assignedStudents.all())
        return super().save(*args, **kwargs)
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
    
    #updates the task's permissions based on the departments and students it is assigned to
    def updatePermissions(self,departmentSet,studentSet):
        #make sure only the given department leaders have task access
        for department in Department.objects.all():
            #if the department is in the given set, give the department leaders access
            if(department in departmentSet and 'manage_task' not in get_perms(department.leaderGroup,self)):
                assign_perm('manage_task',department.leaderGroup,self)
            #otherwise remove access
            elif(department not in departmentSet and 'manage_task' in get_perms(department.leaderGroup,self)):
                remove_perm('manage_task',department.leaderGroup,self)
        #make sure only the given students have task access
        for student in Student.objects.all():
            #if the student is in the given set, give them access
            if(student in studentSet and not student.user.has_perm('manage_task',self)):
                assign_perm('manage_task',student.user,self)
            #otherwise remove access
            elif(student not in studentSet and student.user.has_perm('manage_task',self)):
                remove_perm('manage_task',student.user,self)

#department model
class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    memberGroup = models.OneToOneField(Group,on_delete=models.CASCADE,null=True,blank=True,related_name="member_group")
    leaderGroup = models.OneToOneField(Group,on_delete=models.CASCADE,null=True,blank=True,related_name="leader_group")
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = (
            ('manage_department','Manage department'),
        )
    #on creation, create a group for the department members and leaders
    def save(self,*args,**kwargs):
        #only run if the department is being created, not updated
        if(not self.pk):
            print("department does not yet exist")
            groupName = self.name + "Members"
            leaderGroupName = self.name + "Leaders"
            #create the groups and save them
            self.memberGroup = Group.objects.create(name=groupName)
            self.leaderGroup = Group.objects.create(name=leaderGroupName)

            #give the admin group and leader group permission to manage the department
            adminGroup = Group.objects.get(name='admin')
            assign_perm('manage_department',adminGroup,self)
            assign_perm('manage_department',self.leaderGroup,self)
            
            super().save(*args,**kwargs)
        else:
            kwargs['force_insert'] = False
            kwargs['force_update'] = True
            super().save(*args,**kwargs)
    
    #on deletion delete the associated groups
    def delete(self,*args,**kwargs):
        adminGroup = Group.objects.get(name='admin')
        remove_perm('manage_department',adminGroup,self)
        remove_perm('manage_department',self.leaderGroup,self)

        self.memberGroup.delete()
        self.leaderGroup.delete()
        super().delete(self,*args,**kwargs)
    
    @property
    def member_list(self):
        studentSet = Student.objects.all()
        for student in studentSet:
            if(self.memberGroup not in student.user.groups.all()):
                studentSet = studentSet.exclude(id=student.id)
        return studentSet

    @property
    def leader_list(self):
        studentSet = Student.objects.all()
        for student in studentSet:
            if(self.leaderGroup not in student.user.groups.all()):
                studentSet = studentSet.exclude(id=student.id)
        return studentSet

#each student maps to a django user
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=False,blank=False)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'