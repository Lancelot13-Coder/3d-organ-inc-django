from django.contrib import admin

from .models import Comentario


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("elemento", "texto", "fecha")
    list_filter = ("elemento__categoria",)
