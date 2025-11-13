from django.urls import path
from loger import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signIn , name='task_list'),
    path('signup/', views.signUp, name='signup'),
    path('logout/', views.signOut, name='logout'),
]