from django.test import TestCase
from django.urls import reverse
from task_tracker.models import *
from django.test import Client
from task_tracker.forms import CreateStudentForm

def create_start_groups():
    Group.objects.create(name='student')
    adminGroup = Group.objects.create(name='admin')
    return adminGroup

def create_test_department():
    return Department.objects.create(name="Test",description="This is a test department")
# Create your tests here.
class DepartmentTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.adminGroup = create_start_groups()
        cls.post = create_test_department()
        

    def test_model_content(self):
        self.assertEqual(self.post.name,"Test")
        self.assertEqual(self.post.description,"This is a test department")

    def test_groups_exist(self):
        self.assertEqual(self.post.memberGroup.name,"TestMembers")
        self.assertEqual(self.post.leaderGroup.name,"TestLeaders")

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('department-detail-view',kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)

    def test_url_used(self):
        response = self.client.get(reverse('department-detail-view',kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'task_tracker/department_detail.html')
        self.assertContains(response,'Test Department')

class StudentTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        #create a student using the registerPageview
        cls.adminGroup = create_start_groups()
        cls.department = create_test_department()
        cls.client = Client()

        cls.response = cls.client.post(reverse('student-register-page'),data={'username':'test','first_name':'test','last_name':'test','email':'test@email.com','password1':'t35tPa55word!!','password2':'t35tPa55word!!','departments':[1]})
        
    def test_student_created(self):
        self.student = Student.objects.all()[0]

        self.assertEqual(self.student.first_name,'test')
        self.assertEqual(self.student.last_name,'test')
        self.assertEqual(self.student.user.username,'test')
        self.assertEqual(self.student.user.email,'test@email.com')
        self.assertEqual(self.student.user.groups.get(name='student').name,'student')
        self.assertIn(Group.objects.get(name='TestMembers'),self.student.user.groups.all())
        self.assertEqual(0,1)