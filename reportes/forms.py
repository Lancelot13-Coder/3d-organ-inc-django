"""
Formularios de la app 'reportes'.

Un ModelForm genera automáticamente un formulario HTML a partir de un
modelo. Lo usamos para crear y editar Comentario sin tener que
escribir cada <input> a mano.
"""

from django import forms

from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        # Solo pedimos 'texto': 'elemento' y 'fecha' se asignan solos
        # desde la vista (el elemento viene de la URL, la fecha es
        # automática gracias a default=timezone.now en el modelo).
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(attrs={"rows": 3, "placeholder": "Escribe tu comentario..."}),
        }
        labels = {
            "texto": "Comentario",
        }
