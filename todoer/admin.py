from django.contrib import admin
from .models import Task

# Registrar el modelo Task en el admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "completed", "created_at", "group")
    list_filter = ("completed", "group")
    search_fields = ("title", "description")