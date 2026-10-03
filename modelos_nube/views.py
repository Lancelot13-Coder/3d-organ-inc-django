import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ModeloNubeForm

CLAVE_SESION = "microservicio_activo"
CLAVE_RESILIENTE = "lectura_resiliente"


def _clave_activa(request):
    clave = request.session.get(CLAVE_SESION, settings.MICROSERVICIO_POR_DEFECTO)
    return clave if clave in settings.MICROSERVICIOS else settings.MICROSERVICIO_POR_DEFECTO


def _servicio(request):
    return settings.MICROSERVICIOS[_clave_activa(request)]


def _url_lista(request):
    return _servicio(request)["url"].rstrip("/")


def _url_detalle(request, modelo_id):
    return f"{_url_lista(request)}/{modelo_id}"


def _resiliente_disponible():
    return bool(getattr(settings, "MICROSERVICIO_RESILIENTE_URL", ""))


def _resiliente_activo(request):
    return _resiliente_disponible() and request.session.get(CLAVE_RESILIENTE, True)


def _nombre(clave):
    return settings.MICROSERVICIOS.get(clave, {}).get("nombre", clave)


def _describir_origen(resp):
    """Texto tipo 'Python no respondió; sirvió Go' a partir de las cabeceras del gateway."""
    usado = resp.headers.get("X-Microservicio-Usado")
    if not usado:
        return "Resiliente"
    intentos = [t for t in resp.headers.get("X-Intentos", "").split(";") if ":" in t]
    fallidos = [_nombre(t.split(":")[0]) for t in intentos if t.endswith(":fallo")]
    texto = f"Resiliente → {_nombre(usado)}"
    if fallidos:
        texto += f" (no respondió: {', '.join(fallidos)})"
    return texto


def _leer(request, sufijo=""):
    """GET con resiliencia. Devuelve (datos, origen).

    1) Si la lectura resiliente está activa, consulta el gateway indicándole cuál
       es el servicio preferido (el elegido en los botones).
    2) Si el gateway no responde, consulta directamente el servicio elegido.
    Un 4xx (p. ej. 404) se propaga como error normal.
    """
    clave = _clave_activa(request)
    if _resiliente_activo(request):
        url = settings.MICROSERVICIO_RESILIENTE_URL.rstrip("/") + sufijo
        try:
            resp = requests.get(url, params={"preferido": clave}, timeout=settings.MICROSERVICIO_TIMEOUT)
            if resp.status_code < 500:
                resp.raise_for_status()
                return resp.json(), _describir_origen(resp)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass
    resp = requests.get(_url_lista(request) + sufijo, timeout=settings.MICROSERVICIO_TIMEOUT)
    resp.raise_for_status()
    return resp.json(), f"{_servicio(request)['nombre']} (directo)"


def _contexto(request, **extra):
    """Datos que necesitan todas las pantallas: cuál servicio está activo y los botones."""
    activa = _clave_activa(request)
    contexto = {
        "servicio_activo": _servicio(request),
        "resiliente_disponible": _resiliente_disponible(),
        "resiliente_activo": _resiliente_activo(request),
        "servicios": [
            {"clave": clave, "nombre": datos["nombre"], "activo": clave == activa}
            for clave, datos in settings.MICROSERVICIOS.items()
        ],
    }
    contexto.update(extra)
    return contexto


def _mensaje_error(request, accion, exc):
    texto = f"[{_servicio(request)['nombre']}] No se pudo {accion}: {exc}"
    respuesta = getattr(exc, "response", None)
    if respuesta is not None and respuesta.text:
        # Lo que contestó el microservicio (ayuda a saber la causa real del 500)
        texto += f" | Respuesta del servicio: {respuesta.text[:300]}"
    return texto


@require_POST
def elegir(request):
    clave = request.POST.get("servicio")
    if clave in settings.MICROSERVICIOS:
        request.session[CLAVE_SESION] = clave
    return redirect("modelos_nube:listar")


@require_POST
def alternar_resiliente(request):
    request.session[CLAVE_RESILIENTE] = not _resiliente_activo(request)
    return redirect("modelos_nube:listar")


def listar(request):
    modelos = []
    error = None
    origen = None
    try:
        modelos, origen = _leer(request)
    except requests.exceptions.RequestException as exc:
        error = _mensaje_error(request, "cargar la lista", exc)
    return render(
        request, "modelos_nube/listar.html",
        _contexto(request, modelos=modelos, error=error, origen_lectura=origen),
    )


def crear(request):
    error = None
    if request.method == "POST":
        form = ModeloNubeForm(request.POST)
        if form.is_valid():
            try:
                resp = requests.post(
                    _url_lista(request), json=form.cleaned_data, timeout=settings.MICROSERVICIO_TIMEOUT
                )
                resp.raise_for_status()
                return redirect("modelos_nube:listar")
            except requests.exceptions.RequestException as exc:
                error = _mensaje_error(request, "crear el modelo", exc)
    else:
        form = ModeloNubeForm()
    return render(request, "modelos_nube/form.html", _contexto(request, form=form, modo="crear", error=error))


def editar(request, modelo_id):
    error = None
    if request.method == "POST":
        form = ModeloNubeForm(request.POST)
        if form.is_valid():
            try:
                resp = requests.put(
                    _url_detalle(request, modelo_id), json=form.cleaned_data, timeout=settings.MICROSERVICIO_TIMEOUT
                )
                resp.raise_for_status()
                return redirect("modelos_nube:listar")
            except requests.exceptions.RequestException as exc:
                error = _mensaje_error(request, "actualizar el modelo", exc)
    else:
        try:
            datos, _origen = _leer(request, f"/{modelo_id}")
            form = ModeloNubeForm(initial=datos)
        except requests.exceptions.RequestException as exc:
            error = _mensaje_error(request, "cargar el modelo a editar", exc)
            form = ModeloNubeForm()
    return render(
        request, "modelos_nube/form.html",
        _contexto(request, form=form, modo="editar", modelo_id=modelo_id, error=error),
    )


def eliminar(request, modelo_id):
    error = None
    if request.method == "POST":
        try:
            resp = requests.delete(_url_detalle(request, modelo_id), timeout=settings.MICROSERVICIO_TIMEOUT)
            resp.raise_for_status()
        except requests.exceptions.RequestException as exc:
            error = _mensaje_error(request, "eliminar el modelo", exc)
            return render(request, "modelos_nube/confirmar_eliminar.html", _contexto(request, error=error))
        return redirect("modelos_nube:listar")

    modelo = None
    try:
        modelo, _origen = _leer(request, f"/{modelo_id}")
    except requests.exceptions.RequestException as exc:
        error = _mensaje_error(request, "cargar el modelo", exc)
    return render(
        request, "modelos_nube/confirmar_eliminar.html",
        _contexto(request, modelo=modelo, modelo_id=modelo_id, error=error),
    )
