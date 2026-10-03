from django import forms

CATEGORIAS_SUPABASE = [
    ("🦻 Modelos del Oído", "🦻 Modelos del Oído"),
    ("🤖 Modelos de Prueba", "🤖 Modelos de Prueba"),
]


class ModeloNubeForm(forms.Form):
    nombre = forms.CharField(max_length=150, label="Nombre")
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}), required=False, label="Descripción"
    )
    categoria = forms.ChoiceField(choices=CATEGORIAS_SUPABASE, label="Categoría")
    activo = forms.BooleanField(required=False, initial=True, label="Activo")