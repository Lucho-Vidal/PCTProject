from django.urls import path
from todoer import views
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create_task', views.create_task, name='create_task'),
]