"""
Modelos de la app 'catalogo'.

Sigue la misma lógica que el tutorial02 de Django (modelos Question y
Choice), pero con nombres genéricos de EJEMPLO para que los reemplaces
por las entidades reales de TU problemática.

Idea general (bórrala y reemplázala por la tuya):
    - Categoria  -> agrupa varios "Elemento"
    - Elemento   -> el objeto principal que se lista, se busca y se
                    consulta por id o por categoría.

Ejemplos de qué podrías poner aquí según tu problemática real:
    - Categoria -> "Departamento", Elemento -> "Empleado"
    - Categoria -> "Curso", Elemento -> "Estudiante"
    - Categoria -> "Marca", Elemento -> "Producto"
"""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Categoria(models.Model):
    # EJEMPLO: agrega aquí los campos que necesite tu problemática.
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Genera el slug automáticamente a partir del nombre, así las
        # rutas dinámicas (por categoría) quedan legibles en la URL.
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Elemento(models.Model):
    # EJEMPLO: renombra "Elemento" y sus campos según tu problemática.
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="elementos",
    )
    fecha_registro = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Elemento"
        verbose_name_plural = "Elementos"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return self.nombre

    def fue_registrado_recientemente(self):
        """EJEMPLO de método de modelo, similar a was_published_recently()
        del tutorial. Adapta esta regla de negocio a tu problemática."""
        return self.fecha_registro >= timezone.now() - timezone.timedelta(days=7)
