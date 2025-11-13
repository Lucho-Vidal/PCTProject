from django.db import models

# Create your models here.
# modelo para dos listas de tareas, una para tareas pendientes y otra para tareas completadas.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title