"""
Vistas de la app 'reportes'.

Muestra que una app distinta a 'catalogo' también puede tener varias
vistas propias, y que puede consultar modelos de OTRA app del mismo
proyecto (catalogo.Categoria / catalogo.Elemento) además de los suyos
(Comentario). Esto cumple el requisito de "modelos consultados desde
las vistas" incluso entre apps distintas del mismo proyecto.
"""

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from catalogo.models import Categoria, Elemento
from .forms import ComentarioForm
from .models import Comentario


def resumen(request):
    """Vista 1: panel general con conteos por categoría.
    EJEMPLO: cambia esta consulta según los indicadores que necesite
    tu problemática (totales, promedios, filtros por fecha, etc.)
    """
    categorias_con_totales = Categoria.objects.annotate(total_elementos=Count("elementos"))
    total_elementos = Elemento.objects.count()
    total_comentarios = Comentario.objects.count()
    context = {
        "categorias_con_totales": categorias_con_totales,
        "total_elementos": total_elementos,
        "total_comentarios": total_comentarios,
    }
    return render(request, "reportes/resumen.html", context)


def detalle_categoria(request, categoria_id):
    """Vista 2: reporte de UNA categoría puntual.
    Ruta dinámica con parámetro: /reportes/categoria/<categoria_id>/
    """
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    elementos = categoria.elementos.all()
    context = {"categoria": categoria, "elementos": elementos}
    return render(request, "reportes/detalle_categoria.html", context)


def acerca(request):
    """Vista 3: página estática de ejemplo (sin consultar modelos),
    útil como plantilla para páginas informativas de tu proyecto
    (ayuda, contacto, políticas, etc.)
    """
    return render(request, "reportes/acerca.html")


# --- CRUD de comentarios, disponible desde la página normal (sin admin) ---

def crear_comentario(request, elemento_id):
    """CREATE: formulario para agregar un comentario a un Modelo 3D
    puntual. 'elemento_id' llega por la URL (ruta dinámica), igual que
    en las vistas de 'catalogo'.
    """
    elemento = get_object_or_404(Elemento, pk=elemento_id)

    if request.method == "POST":
        # El usuario envió el formulario: validamos y guardamos.
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)  # aún no lo guarda en la BD
            comentario.elemento = elemento          # asignamos el elemento nosotros
            comentario.save()                       # ahora sí, a la base sqlite
            return redirect("catalogo:detalle", elemento_id=elemento.id)
    else:
        # Primera visita a la página: mostramos el formulario vacío.
        form = ComentarioForm()

    context = {"form": form, "elemento": elemento, "modo": "crear"}
    return render(request, "reportes/comentario_form.html", context)


def editar_comentario(request, comentario_id):
    """UPDATE: formulario pre-llenado con los datos actuales del
    comentario (instance=comentario), para modificarlo.
    """
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect("catalogo:detalle", elemento_id=comentario.elemento.id)
    else:
        form = ComentarioForm(instance=comentario)

    context = {"form": form, "elemento": comentario.elemento, "modo": "editar"}
    return render(request, "reportes/comentario_form.html", context)


def eliminar_comentario(request, comentario_id):
    """DELETE: pide confirmación antes de borrar (buena práctica: nunca
    borres directo con un GET, siempre confirma con POST).
    """
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    elemento_id = comentario.elemento.id

    if request.method == "POST":
        comentario.delete()
        return redirect("catalogo:detalle", elemento_id=elemento_id)

    context = {"comentario": comentario}
    return render(request, "reportes/comentario_confirmar_eliminar.html", context)
