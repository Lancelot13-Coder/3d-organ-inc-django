"""
URLconf de la app 'catalogo'.

app_name define un 'namespace' para poder usar {% url 'catalogo:detalle' %}
en los templates sin choques de nombres con otras apps (ver tutorial03,
sección "Removing hardcoded URLs in templates" / namespacing de URLs).
"""

from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    # /catalogo/
    path("", views.index, name="index"),
    # /catalogo/buscar/
    path("buscar/", views.buscar, name="buscar"),
    # /catalogo/categoria/<categoria_slug>/  -> ruta dinámica (texto)
    path("categoria/<slug:categoria_slug>/", views.por_categoria, name="por_categoria"),
    # /catalogo/<elemento_id>/  -> ruta dinámica (número)
    path("<int:elemento_id>/", views.detalle, name="detalle"),
]
