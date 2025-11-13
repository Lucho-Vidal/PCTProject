from django.urls import path
from todoer import views
urlpatterns = [
    path('signin/', views.task_list, name='task_list'),
]