from django import forms
from django.contrib.auth.models import Group

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=True,
        empty_label="Seleccione grupo"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Orden jerárquico
        hierarchy = ["administrador", "jefatura", "supervisor", "visor"]

        if user:
            # Buscar el grupo más alto del usuario
            user_groups = list(user.groups.values_list("name", flat=True))
            for g in hierarchy:
                if g in user_groups:
                    max_group = g
                    break

            # Filtrar grupos permitidos
            idx = hierarchy.index(max_group)
            allowed = hierarchy[idx:]  # desde su nivel hacia abajo
            self.fields["group"].queryset = Group.objects.filter(name__in=allowed)