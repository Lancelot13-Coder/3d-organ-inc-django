"""
Vistas de la app 'integracion'.

Esto ilustra un patrón DISTINTO al de 'catalogo' y 'reportes':
en vez de que la vista consulte el ORM de Django (una base de datos
local vía modelos), la vista hace una petición HTTP a un
MICROSERVICIO tuyo, desplegado en la nube (ej. Render o Railway),
que es quien realmente habla con la base de datos en la nube
(Supabase). Django solo consume ese microservicio como si fuera
cualquier API externa.

Flujo completo:
    Navegador
        -> Django (esta vista, datos_externos)
            -> HTTP GET a settings.MICROSERVICIO_URL
                -> tu microservicio (Render/Railway)
                    -> consulta Supabase (Postgres en la nube)
                <- responde JSON
            <- Django recibe el JSON con 'requests'
        <- Django arma el context y renderiza el template
    <- el navegador ve la página final

EJEMPLO: cuando tengas tu microservicio real desplegado, solo
necesitas cambiar la URL en la variable de entorno MICROSERVICIO_URL
(ver config/settings.py) — no hay que tocar esta vista.
"""

import requests
from django.conf import settings
from django.shortcuts import render


def datos_externos(request):
    """Consume un endpoint HTTP externo (tu microservicio) y muestra
    lo que devuelva. Maneja también el caso en que el microservicio
    no responda (para que la página no se rompa mientras lo desarrollas).
    """
    url = settings.MICROSERVICIO_URL
    datos = None
    error = None

    try:
        # timeout es importante: si el microservicio no responde,
        # Django no debe quedarse esperando indefinidamente.
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()  # lanza excepción si el status no es 2xx
        datos = respuesta.json()
    except requests.exceptions.RequestException as exc:
        # Cubre: microservicio caído, URL de EJEMPLO todavía sin reemplazar,
        # tiempo de espera agotado, respuesta que no es JSON válido, etc.
        error = str(exc)

    context = {
        "url_microservicio": url,
        "datos": datos,
        "error": error,
    }
    return render(request, "integracion/datos_externos.html", context)
