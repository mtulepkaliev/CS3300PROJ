from django.urls import path
from django.conf.urls import include
from . import views
from . import task_views
from . import department_views
from . import student_views

urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
path('', views.index, name='index'),
path('task_list/', task_views.taskListView.as_view(), name='task-list-view'),
path('task_list/department/<int:department_id>', task_views.taskListView.as_view(), name='task-list-department-view'),
path('task/<int:pk>/', task_views.taskDetailView.as_view(), name='task-detail-view'),
path('task/create/', task_views.taskCreateView, name='task-create-view'),
path('task/<int:pk>/update/', task_views.taskUpdateView, name='task-update-view'),
path('task/<int:pk>/delete/', task_views.taskDeleteView, name='task-delete-view'),
path('task/<int:pk>/toggle_complete/', task_views.taskToggleCompleteView, name='task-toggle-complete-view'),

path('departments/',department_views.departmentListView.as_view(),name='department-list-view'),
path('departments/<int:pk>/',department_views.departmentDetailView.as_view(),name='department-detail-view'),
path('departments/create/',department_views.departmentCreateView,name='department-create-view'),
path('departments/delete/<int:pk>',department_views.departmentDeleteView,name='department-delete-view'),
path('departments/update/<int:pk>',department_views.departmentUpdateView,name='department-update-view'),

path('students/register',student_views.registerPage,name='student-register-page'),
path('students/<int:pk>/',student_views.studentDetailView.as_view(),name='student-detail-view'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
