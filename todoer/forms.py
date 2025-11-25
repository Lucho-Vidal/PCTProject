from django import forms
from .models import Task
from django.contrib.auth.models import Group

class CreateNewTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "group","completed"]

    # Opcional: limitar los grupos a los que ya creaste
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=["administrador", "jefatura", "supervisor", "visor"]),
        required=False,
        empty_label="(Tarea propia)"
    )