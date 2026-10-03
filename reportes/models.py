"""
Modelos de la app 'reportes'.

EJEMPLO de cómo una segunda app puede tener su propio modelo y, al
mismo tiempo, relacionarse con modelos de otra app del proyecto
(catalogo.Elemento). Reemplaza esto por lo que necesite tu problemática
(por ejemplo: registro de incidencias, comentarios, movimientos, etc.)
"""

from django.db import models
from django.utils import timezone

from catalogo.models import Elemento


class Comentario(models.Model):
    elemento = models.ForeignKey(
        Elemento,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    texto = models.CharField(max_length=300)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Comentario sobre {self.elemento.nombre}"
