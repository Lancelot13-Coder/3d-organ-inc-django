from django.urls import path

from . import views

app_name = "integracion"

urlpatterns = [
    # /microservicio/
    path("", views.datos_externos, name="datos_externos"),
]
