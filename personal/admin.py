from django.contrib import admin

from .models import Empleado, Categoria

# Registrar el modelo Task en el admin
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("apellido","nombre")
    # list_filter = ("categoria")
    # search_fields = ("title", "description")
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("categoria",)