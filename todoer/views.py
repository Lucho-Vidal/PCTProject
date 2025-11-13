from django.shortcuts import render
from .models import Task

# Create your views here.
def task_list(request):
    pending_tasks = Task.objects.filter(completed=False).order_by('-created_at')
    completed_tasks = Task.objects.filter(completed=True).order_by('-created_at')
    return render(request, 'todoer/task_list.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks
    })