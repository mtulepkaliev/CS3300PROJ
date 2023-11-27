from django.test import TestCase
from django.urls import reverse
from task_tracker.models import *
from django.test import Client
from task_tracker.forms import CreateStudentForm
from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep




def create_start_groups():
    Group.objects.create(name='student')
    adminGroup = Group.objects.create(name='admin')
    return adminGroup

def create_test_department(dept_name='Test',dept_description='This is a test department'):
    return Department.objects.create(name=dept_name,description=dept_description)

def create_test_student():
    return Student.objects.create(first_name='test',last_name='test',user=User.objects.create_user(username='test',email="test@email.com",password="t35tPa55word!!"))
# Create your tests here.
class DepartmentTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.adminGroup = create_start_groups()
        cls.post = create_test_department()
        

    def test_model_content(self):
        print("Testing Department model content:\n")
        self.assertEqual(self.post.name,"Test")
        self.assertEqual(self.post.description,"This is a test department")

    def test_groups_exist(self):
        print("Testing Department groups exist:\n")
        self.assertEqual(self.post.memberGroup.name,"TestMembers")
        self.assertEqual(self.post.leaderGroup.name,"TestLeaders")

    def test_url_accessible_by_name(self):
        print("Testing Department url accessible by name:\n")
        response = self.client.get(reverse('department-detail-view',kwargs={'pk':1}))
        self.assertEqual(response.status_code,200)

    def test_url_used(self):
        print("Testing Department url used:\n")
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
        print("Testing Student created:\n")
        self.student = Student.objects.all()[0]

        self.assertEqual(self.student.first_name,'test')
        self.assertEqual(self.student.last_name,'test')
        self.assertEqual(self.student.user.username,'test')
        self.assertEqual(self.student.user.email,'test@email.com')
        self.assertEqual(self.student.user.groups.get(name='student').name,'student')
        self.assertIn(Group.objects.get(name='TestMembers'),self.student.user.groups.all())


# https://python.plainenglish.io/django-selenium-writing-integration-tests-21e2051c65b8
class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

#https://www.selenium.dev/documentation/webdriver/elements/finders/
class CreateUserTestCase(SeleniumTestCase):
    def test_create_user(self):
        print("Testing create user with selenium:\n")
        create_start_groups()
        create_test_department()
        self.driver.get(f"{self.live_server_url}{reverse('student-register-page')}")
        self.driver.find_element(By.NAME,"username").send_keys("test")
        self.driver.find_element(By.NAME,"first_name").send_keys("test")
        self.driver.find_element(By.NAME,"last_name").send_keys("test")
        self.driver.find_element(By.NAME,"email").send_keys("email@test.com")
        self.driver.find_element(By.NAME,"password1").send_keys("t35tPa55word!!")
        self.driver.find_element(By.NAME,"password2").send_keys("t35tPa55word!!")


        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        department_checkboxes = self.driver.find_elements(By.CLASS_NAME,"form-check-input")
        for checkbox in department_checkboxes:
             #https://stackoverflow.com/questions/44912203/selenium-web-driver-java-element-is-not-clickable-at-point-x-y-other-elem
            WebDriverWait(self.driver,10).until(EC.visibility_of(checkbox))
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(checkbox))
            checkbox.send_keys("")
            checkbox.click()
            WebDriverWait(self.driver,10).until(EC.element_selection_state_to_be(checkbox,True))
        self.driver.find_element(By.NAME,"password2").submit()

        WebDriverWait(self.driver,10).until(EC.url_contains("login"))
        self.student = Student.objects.all()[0]
        self.assertEqual(self.student.first_name,'test')
        self.assertIn(Department.objects.all()[0].memberGroup,self.student.user.groups.all())

class LoginTestCase(SeleniumTestCase):
    def test_created_user_can_login(self):
        print("Testing login with selenium:\n")
        create_start_groups()
        create_test_department()
        create_test_student()   

        #enter data
        self.driver.get(f"{self.live_server_url}{reverse('login')}")
        self.driver.find_element(By.NAME,"username").send_keys("test")
        self.driver.find_element(By.NAME,"password").send_keys("t35tPa55word!!")

        self.driver.find_element(By.NAME,"password").submit()

        #check redirect upon succesful login
        WebDriverWait(self.driver,10).until(EC.url_contains("students"))

class DepartmentListTestCase(SeleniumTestCase):
    def test_department_list(self):
        print("Testing department list page with selenium:\n")
        create_start_groups()
        create_test_department()
        self.driver.get(f"{self.live_server_url}{reverse('department-list-view')}")
        self.assertIn("Departments",self.driver.page_source)
        self.assertIn("Test",self.driver.page_source)
        self.assertIn("This is a test department",self.driver.page_source)
    