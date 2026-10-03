"""
URLconf raíz del proyecto (ver tutorial01 - 'URL dispatcher').

Aquí solo se declara EN QUÉ PREFIJO vive cada app. El detalle de cada
ruta se resuelve dentro del urls.py de cada app (catalogo/urls.py y
reportes/urls.py), usando include(), tal como recomienda la
documentación de Django.
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # EJEMPLO: cambia estos prefijos por los que tenga sentido en tu
    # problemática (ej: "inventario/", "clientes/", "tickets/", etc.)
    path("catalogo/", include("catalogo.urls")),
    path("reportes/", include("reportes.urls")),
    path("microservicio/", include("integracion.urls")),
    path("admin/", admin.site.urls),
    path('', RedirectView.as_view(url='catalogo/', permanent=False)),
    path("asistente/", include("asistente_ia.urls")),
    path("nube/", include("modelos_nube.urls")),
]
