from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
path('', views.index, name='index'),
path('task_list/', views.taskListView.as_view(), name='task-list-view'),
path('task_list/<int:department_id>', views.taskListView.as_view(), name='task-list-department-view'),
path('task/<int:pk>/', views.taskDetailView.as_view(), name='task-detail-view'),
path('task/create/', views.taskCreateView, name='task-create-view'),
path('task/<int:pk>/update/', views.taskUpdateView, name='task-update-view'),
path('task/<int:pk>/delete/', views.taskDeleteView, name='task-delete-view'),
path('task/<int:pk>/toggle_complete/', views.taskToggleCompleteView, name='task-toggle-complete-view'),
path('departments/<int:pk>/',views.departmentDetailView.as_view(),name='department-detail-view'),
path('students/register',views.registerPage,name='student-register-page'),
path('departments/create/',views.departmentCreateView,name='department-create-view'),
path('students/<int:pk>/',views.studentDetailView.as_view(),name='student-detail-view'),
path('departments/',views.departmentListView.as_view(),name='department-list-view'),
path('departments/delete/<int:pk>',views.departmentDeleteView,name='department-delete-view'),
path('departments/update/<int:pk>',views.departmentUpdateView,name='department-update-view'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
