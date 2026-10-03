from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    # /reportes/
    path("", views.resumen, name="resumen"),
    # /reportes/categoria/<categoria_id>/ -> ruta dinámica (número)
    path("categoria/<int:categoria_id>/", views.detalle_categoria, name="detalle_categoria"),
    # /reportes/acerca/
    path("acerca/", views.acerca, name="acerca"),
    # --- CRUD de comentarios ---
    # /reportes/comentario/nuevo/<elemento_id>/
    path("comentario/nuevo/<int:elemento_id>/", views.crear_comentario, name="crear_comentario"),
    # /reportes/comentario/<comentario_id>/editar/
    path("comentario/<int:comentario_id>/editar/", views.editar_comentario, name="editar_comentario"),
    # /reportes/comentario/<comentario_id>/eliminar/
    path("comentario/<int:comentario_id>/eliminar/", views.eliminar_comentario, name="eliminar_comentario"),
]
