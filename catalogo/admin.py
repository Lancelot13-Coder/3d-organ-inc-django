from django.contrib import admin

from .models import Categoria, Elemento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Elemento)
class ElementoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "fecha_registro", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre", "descripcion")
