"""
Vistas de la app 'catalogo'.

Aquí se aplican las ideas del tutorial03 de Django:
    - Varias vistas dentro de una misma app (index, detalle, por_categoria...).
    - Vistas que reciben parámetros desde la URL (rutas dinámicas).
    - Vistas que consultan los modelos (Categoria, Elemento) y arman
      un 'context' para pasarlo a un template con render().
    - get_object_or_404 para responder 404 automáticamente si el
      parámetro de la URL no corresponde a ningún registro.
"""

from django.shortcuts import get_object_or_404, render

from .models import Categoria, Elemento
# Importamos un modelo de OTRA app (reportes) directamente en la vista,
# para dejar bien claro el patrón: view -> consulta model -> arma context.
from reportes.models import Comentario


def index(request):
    """Vista 1: lista general.
    EJEMPLO: aquí decides qué mostrar primero (los últimos elementos,
    un resumen, etc.) según tu problemática real.
    """
    lista_elementos = Elemento.objects.filter(activo=True).order_by("-fecha_registro")[:20]
    categorias = Categoria.objects.all()
    context = {
        "lista_elementos": lista_elementos,
        "categorias": categorias,
    }
    return render(request, "catalogo/index.html", context)


def detalle(request, elemento_id):
    """Vista 2: detalle de UN elemento.
    Ruta dinámica con parámetro: /catalogo/<elemento_id>/
    'elemento_id' llega directamente desde urls.py (int:elemento_id).
    """
    elemento = get_object_or_404(Elemento, pk=elemento_id)

    # Patrón view -> model -> context:
    # 1) la vista consulta el modelo Comentario filtrando por el elemento actual
    comentarios = Comentario.objects.filter(elemento=elemento)
    # 2) arma el context con TODO lo que el template necesita
    context = {
        "elemento": elemento,
        "comentarios": comentarios,
    }
    # 3) render() entrega el template + context ya combinados
    return render(request, "catalogo/detalle.html", context)


def por_categoria(request, categoria_slug):
    """Vista 3: filtra elementos según la categoría indicada en la URL.
    Ruta dinámica con parámetro de texto (slug):
    /catalogo/categoria/<categoria_slug>/

    Esta vista SÍ 'hace algo' con el parámetro recibido: lo usa para
    filtrar el queryset de Elemento, que es justo lo que pide el
    requisito de 'rutas dinámicas + vista que procese esa información'.
    """
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    # prefetch_related trae de una vez los comentarios de cada elemento
    # (evita hacer una consulta nueva a la BD por cada elemento al recorrer
    # el template con {% for %}).
    elementos = categoria.elementos.filter(activo=True).prefetch_related("comentarios")
    context = {
        "categoria": categoria,
        "elementos": elementos,
    }
    return render(request, "catalogo/por_categoria.html", context)


def buscar(request):
    """Vista 4 (EJEMPLO extra): búsqueda simple por texto usando
    querystring, ej: /catalogo/buscar/?q=algo
    Útil para mostrar otra forma de recibir datos además de la URL
    dinámica (path converters) que ya usan 'detalle' y 'por_categoria'.
    """
    consulta = request.GET.get("q", "").strip()
    resultados = []
    if consulta:
        resultados = Elemento.objects.filter(nombre__icontains=consulta)
    context = {"consulta": consulta, "resultados": resultados}
    return render(request, "catalogo/buscar.html", context)
