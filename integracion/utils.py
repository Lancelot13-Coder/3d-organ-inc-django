"""
Utilidad de RESILIENCIA compartida.

Idea: cuando el sitio necesita LEER datos de la nube, primero intenta
con el microservicio principal (Python/Render). Si ese falla por
cualquier motivo (caído, timeout, error 5xx...), reintenta
automáticamente con el microservicio de respaldo, escrito en un
lenguaje distinto (Node.js/Netlify), para que el usuario nunca vea un
error si al menos uno de los dos servicios sigue funcionando.

Esto demuestra resiliencia entre microservicios de distintos lenguajes:
si Python cae, Node.js sigue respondiendo (y viceversa, si algún día
agregas el mismo respaldo en la otra dirección).
"""

import requests


def leer_con_resiliencia(url_principal, url_respaldo, timeout=8):
    """Devuelve (datos, error, fuente).

    - Si el principal responde bien: (datos, None, "python")
    - Si el principal falla pero el respaldo responde: (datos, None, "node (respaldo)")
    - Si ambos fallan: (None, "mensaje con ambos errores", None)
    """
    try:
        r = requests.get(url_principal, timeout=timeout)
        r.raise_for_status()
        return r.json(), None, "python"
    except requests.exceptions.RequestException as error_python:
        if not url_respaldo:
            return None, str(error_python), None
        try:
            r = requests.get(url_respaldo, timeout=timeout)
            r.raise_for_status()
            return r.json(), None, "node (respaldo)"
        except requests.exceptions.RequestException as error_node:
            mensaje = (
                f"Fallaron ambos microservicios. "
                f"Python: {error_python} | Node.js: {error_node}"
            )
            return None, mensaje, None