from django.db import models

# Create your models here.
# modelo para dos listas de tareas, una para tareas pendientes y otra para tareas completadas.
from django.db import models
from django.contrib.auth.models import User, Group

# class Task(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False)

#     # 🔑 Relación con el usuario que creó la tarea
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

#     # 🔑 Si la tarea es grupal, se asocia a un grupo
#     group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")

#     # 🔑 Campo para distinguir si es propia o grupal
#     is_group_task = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

#     def can_edit(self, user: User) -> bool:
#         """
#         Lógica de permisos:
#         - Si es grupal: cualquier miembro del grupo puede editar.
#         - Si es propia: solo el dueño puede editar.
#         """
#         if self.is_group_task and self.group:
#             return user in self.group.user_set.all()
#         return user == self.owner

#     def can_view(self, user: User) -> bool:
#         """
#         Lógica de visibilidad:
#         - Si es grupal: cualquier miembro del grupo puede verla.
#         - Si es propia: solo el dueño puede verla.
#         """
#         if self.is_group_task and self.group:
#             return user in self.group.user_set.all()
#         return user == self.owner
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    # Usuario que creó la tarea
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    # Grupo asignado (Administrador, Jefatura, Supervisor, Visor)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 👈 cuándo se modificó
    last_edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_tasks"  # 👈 quién lo modificó
    )


    def __str__(self):
        return self.title

    def can_view(self, user: User) -> bool:
        """Un usuario puede ver la tarea si:
        - Es el dueño
        - Pertenece al grupo asignado
        """
        if self.group:
            return user in self.group.user_set.all()
        return user == self.owner

    def can_edit(self, user: User) -> bool:
        """Un usuario puede editar la tarea si:
        - Es el dueño
        - Pertenece al grupo asignado
        """
        if self.group:
            return user in self.group.user_set.all()
        return user == self.owner
