import requests
from django.conf import settings
from django.shortcuts import render

from catalogo.models import Elemento
from reportes.models import Comentario

CONTEXTO_DEL_SITIO = (
    "Eres un asistente educativo del sitio 3D-Organ-Inc, una plataforma "
    "sobre bioimpresión 3D de órganos aplicada a la medicina "
    "regenerativa. A continuación tienes datos REALES tomados de la "
    "base de datos del sitio (local) y de un microservicio en la nube "
    "(Supabase). Úsalos para responder con precisión. Si la pregunta "
    "no se puede responder con estos datos, dilo con honestidad en vez "
    "de inventar. Responde en español, de forma clara y breve."
)

LIMITE_REGISTROS = 30


def _contexto_local():
    elementos = Elemento.objects.select_related("categoria").filter(activo=True)[:LIMITE_REGISTROS]
    if not elementos:
        return "BASE DE DATOS LOCAL (Django/SQLite): no hay Modelos 3D registrados todavía."
    lineas = ["BASE DE DATOS LOCAL (Django/SQLite) — Modelos 3D:"]
    for e in elementos:
        cantidad_comentarios = Comentario.objects.filter(elemento=e).count()
        lineas.append(
            f"- '{e.nombre}' (categoría: {e.categoria.nombre}): "
            f"{e.descripcion or 'sin descripción'}. "
            f"Tiene {cantidad_comentarios} comentario(s)."
        )
    return "\n".join(lineas)


def _contexto_nube():
    try:
        resp = requests.get(settings.MICROSERVICIO_URL, timeout=10)
        resp.raise_for_status()
        modelos = resp.json()
    except requests.exceptions.RequestException as exc:
        return f"MICROSERVICIO EN LA NUBE (Supabase): no se pudo consultar ahora mismo ({exc})."
    if not modelos:
        return "MICROSERVICIO EN LA NUBE (Supabase): no hay Modelos 3D registrados todavía."
    lineas = ["MICROSERVICIO EN LA NUBE (Supabase) — Modelos 3D:"]
    for m in modelos[:LIMITE_REGISTROS]:
        estado = "activo" if m.get("activo") else "inactivo"
        lineas.append(
            f"- '{m.get('nombre')}' (categoría: {m.get('categoria')}, {estado}): "
            f"{m.get('descripcion') or 'sin descripción'}."
        )
    return "\n".join(lineas)


def preguntar(request):
    pregunta = ""
    respuesta = None
    error = None

    if request.method == "POST":
        pregunta = request.POST.get("pregunta", "").strip()
        if not pregunta:
            error = "Escribe una pregunta antes de enviar."
        else:
            contexto_completo = "\n\n".join([
                CONTEXTO_DEL_SITIO,
                _contexto_local(),
                _contexto_nube(),
            ])
            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{settings.IA_MODELO}:generateContent"
            )
            headers = {"Content-Type": "application/json"}
            params = {"key": settings.IA_API_KEY}
            cuerpo = {"contents": [{"parts": [{"text": f"{contexto_completo}\n\nPregunta del usuario: {pregunta}"}]}]}
            try:
                resp = requests.post(url, headers=headers, params=params, json=cuerpo, timeout=20)
                resp.raise_for_status()
                datos = resp.json()
                respuesta = datos["candidates"][0]["content"]["parts"][0]["text"]
            except requests.exceptions.RequestException as exc:
                error = f"No se pudo contactar a la IA: {exc}"
            except (KeyError, IndexError):
                error = "La IA respondió, pero en un formato inesperado."

    context = {"pregunta": pregunta, "respuesta": respuesta, "error": error}
    return render(request, "asistente_ia/preguntar.html", context)