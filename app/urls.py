"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ecodoc import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',include('ecodoc.urls')),
    path('add/',views.add_employee,name="add_emp"),
    path('save_task/', views.save_task, name='save_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('move_task_to_column/', views.move_task_to_column, name='move_task_to_column'),
    path('load_tasks/', views.get_tasks_from_firebase, name='load_tasks'),
    path('add_task_todo/', views.add_task_todo, name='add_task_todo'),
    path('load_tasks_todo/', views.load_tasks_todo, name='load_tasks_todo'),
    path('delete_tasks_todo/', views.delete_task_todo, name='delete_tasks_todo'),
    path('add/',views.add_employee,name="add_emp"),
    path('add_project/',views.add_project,name="add_pro"),
    
]
