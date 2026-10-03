#!/usr/bin/env python
"""Utilidad de línea de comandos de Django (equivalente al manage.py
que genera 'django-admin startproject')."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? "
            "¿Olvidaste activar el entorno virtual (venv)?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
