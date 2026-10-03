"""
Esta app NO tiene modelos propios a propósito: su función es
consumir datos desde un microservicio externo (que tú vas a
desplegar en Render/Railway y que a su vez habla con Supabase),
no guardar nada en la base de datos local (SQLite) de este proyecto.
"""

from django.db import models  # noqa: F401  (se deja el import por si luego agregas un modelo, ej. para cachear respuestas)
