from django.urls import path

from . import views

app_name = "asistente_ia"

urlpatterns = [
    path("", views.preguntar, name="preguntar"),
]