from django.urls import path
from todoer import views
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create_task', views.create_task, name='create_task'),
    path("<int:task_id>/", views.task_detail, name="task_detail"),
    path("<int:task_id>/edit/", views.edit_task, name="edit_task"),
    path("<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("<int:task_id>/toggle/", views.toggle_task_completed, name="toggle_task_completed"),
]