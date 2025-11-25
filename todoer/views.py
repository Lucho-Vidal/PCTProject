from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import CreateNewTask
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
import json

# Create your views here.
def task_list(request):
    # Tareas propias
    own_tasks = Task.objects.filter(owner=request.user)

    # Tareas grupales donde el usuario pertenece al grupo
    group_tasks = Task.objects.filter(group__in=request.user.groups.all())

    pending_tasks = (own_tasks | group_tasks).filter(completed=False).order_by("-created_at")
    completed_tasks = (own_tasks | group_tasks).filter(completed=True).order_by("-created_at")

    return render(request, "todoer/task_list.html", {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks
    })

def create_task(request):
    if request.method == "POST":
        form = CreateNewTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # asignar el dueño
            task.save()
            log_action(request.user, task, ADDITION, "La tarea fue creada desde la app")
            return redirect("todoer:task_list")
    else:
        form = CreateNewTask()
    return render(request, "todoer/create_task.html", {"form": form})

# Vista detalle
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Traer el histórico de cambios de este objeto
    content_type = ContentType.objects.get_for_model(Task)
    history = LogEntry.objects.filter(
        content_type=content_type,
        object_id=task.id
    ).order_by("-action_time")

    # Validar permisos: solo dueño o miembros del grupo
    if not task.can_view(request.user):
        return redirect("todoer:task_list")
    
    # Parsear mensajes
    for entry in history:
        try:
            entry.parsed_message = json.loads(entry.change_message)
        except Exception:
            entry.parsed_message = entry.change_message

    return render(request, "todoer/task_detail.html", {
        "task": task,
        "history": history
        })


# Vista edición
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Validar permisos
    if not task.can_edit(request.user):
        return redirect("todoer:task_list")

    if request.method == "POST":
        form = CreateNewTask(request.POST, instance=task)
        if form.is_valid():
            edited_task = form.save(commit=False)
            edited_task.last_edited_by = request.user  # 👈 guardamos quién editó
            edited_task.save()
            log_action(request.user, edited_task, CHANGE, "Campos modificados desde la app")


            return redirect("todoer:task_detail", task_id=task.id)
    else:
        form = CreateNewTask(instance=task)

    return render(request, "todoer/edit_task.html", {"form": form, "task": task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Solo permitir si el usuario puede editar/eliminar
    if not task.can_edit(request.user):
        return redirect("todoer:task_list")

    # Registrar antes de borrar
    log_action(request.user, task, DELETION, "La tarea fue eliminada desde la app")

    task.delete()
    return redirect("todoer:task_list")

def log_action(user, obj, flag, message=""):
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=flag,
        change_message=message,
    )

def toggle_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.can_edit(request.user):
        task.completed = not task.completed
        task.save()
        log_action(request.user, task, CHANGE, "La tarea cambio de estado desde la app")

    return redirect("todoer:task_list")
