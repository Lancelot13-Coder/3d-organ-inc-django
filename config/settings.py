"""
Configuración del proyecto 'config'.

Este archivo nace del tutorial oficial de Django (tutorial01) y se
extiende con lo visto en tutorial02 (base de datos / apps instaladas)
y tutorial03 (templates).

NOTA PARA TI: cambia el nombre del proyecto, el idioma, la zona horaria,
etc. según tu problemática real. Aquí se deja tal cual lo genera
'django-admin startproject' más los ajustes mínimos de los tutoriales.
"""

import os
from pathlib import Path

# Construye rutas dentro del proyecto así: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ADVERTENCIA DE SEGURIDAD: mantén en secreto la clave usada en producción.
# En un proyecto real, esto NO debe subirse a un repositorio público;
# usa variables de entorno (por ejemplo con python-decouple o django-environ).
SECRET_KEY = "clave-de-ejemplo-cambia-esto-antes-de-producción"

# ADVERTENCIA DE SEGURIDAD: no ejecutes con DEBUG activado en producción.
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
_host_render = os.environ.get("RENDER_EXTERNAL_HOSTNAME")  # Render lo define solo
if _host_render:
    ALLOWED_HOSTS.append(_host_render)
CSRF_TRUSTED_ORIGINS = [f"https://{_host_render}"] if _host_render else []


# Definición de aplicaciones -------------------------------------------------
# Aquí se ve claramente que UN proyecto puede contener VARIAS apps:
# 'catalogo' y 'reportes' son dos apps propias de este proyecto,
# además de las apps que trae Django por defecto (admin, auth, etc.)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # --- Apps propias del proyecto (EJEMPLO, agrega o renombra las tuyas) ---
    "catalogo",
    "reportes",
    "integracion",
    "asistente_ia",
    "modelos_nube",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # sirve los estáticos en Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 'templates/' a nivel de proyecto, para una plantilla base
        # compartida por todas las apps (tutorial03 permite ambos enfoques:
        # templates por app y templates a nivel de proyecto).
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Base de datos ---------------------------------------------------------
# Por defecto SQLite, tal como lo deja el tutorial oficial (tutorial02).
import dj_database_url

# Sin DATABASE_URL usa SQLite (local). Con DATABASE_URL usa PostgreSQL (Render/Supabase).
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Validación de contraseñas ----------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internacionalización ----------------------------------------------------
# EJEMPLO: cámbialo si tu problemática está en otro idioma / zona horaria.
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True


# Archivos estáticos (CSS, JavaScript, imágenes) ---------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Microservicio externo (app 'integracion') --------------------------------
# Se lee de una variable de entorno para NO dejar la URL final "quemada"
# en el código; si no defines la variable, usa el placeholder de ejemplo.
MICROSERVICIO_URL = os.environ.get(
    "MICROSERVICIO_URL",
    "https://threed-organ-inc-microservicio.onrender.com/api/modelos",
)

# Los 4 microservicios disponibles para la app 'modelos_nube'. El usuario
# elige con cuál trabajar desde los botones de la pantalla de Modelos en la
# Nube. Cada URL puede cambiarse con su variable de entorno.
MICROSERVICIOS = {
    "python": {
        "nombre": "Python",
        "url": MICROSERVICIO_URL,
    },
    "node": {
        "nombre": "Node.js",
        "url": os.environ.get(
            "MICROSERVICIO_NODE_URL",
            "https://threed-organ-inc-microservicio-node.onrender.com/api/modelos",
        ),
    },
    "java": {
        "nombre": "Java",
        "url": os.environ.get(
            "MICROSERVICIO_JAVA_URL",
            "https://threed-organ-inc-microservicio-java.onrender.com/api/modelos",
        ),
    },
    "go": {
        "nombre": "Go",
        "url": os.environ.get(
            "MICROSERVICIO_GO_URL",
            "https://threed-organ-inc-microservicio-go.onrender.com/api/modelos",
        ),
    },
}
MICROSERVICIO_POR_DEFECTO = "python"

# Microservicio RESILIENTE (gateway de solo lectura). Cuando está activado, las
# lecturas (listar, cargar para editar/eliminar) pasan primero por él: si el
# servicio elegido falla, el gateway responde con otro. Déjalo vacío ("") para
# desactivar la función.
MICROSERVICIO_RESILIENTE_URL = os.environ.get(
    "MICROSERVICIO_RESILIENTE_URL",
    "https://threed-organ-inc-microservicio-resiliente.onrender.com/api/modelos",
)
# Render (plan gratis) tarda hasta ~60 s en despertar un servicio dormido.
MICROSERVICIO_TIMEOUT = 60



IA_API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")
IA_MODELO = os.environ.get("GOOGLE_AI_MODELO", "gemini-flash-latest")