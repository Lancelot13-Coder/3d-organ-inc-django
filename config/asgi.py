"""
Configuración ASGI para el proyecto 'config'.
Generado de forma equivalente a 'django-admin startproject'.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
