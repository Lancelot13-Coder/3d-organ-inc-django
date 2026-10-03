from django.urls import path

from . import views

app_name = "modelos_nube"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("elegir/", views.elegir, name="elegir"),
    path("resiliente/", views.alternar_resiliente, name="resiliente"),
    path("nuevo/", views.crear, name="crear"),
    path("<int:modelo_id>/editar/", views.editar, name="editar"),
    path("<int:modelo_id>/eliminar/", views.eliminar, name="eliminar"),
]
