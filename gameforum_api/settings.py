# gameforum_api/settings.py

import os
from pathlib import Path
import dj_database_url
import graphene_file_upload.scalars

# ─── BASE ───────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'replace-this-for-development-only'
)  # En Render deberás inyectar SECRET_KEY real vía variables de entorno

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hosts permitidos (en Render pon tu dominio: "tu-app.onrender.com")
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# ─── APPS & MIDDLEWARE ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORS
    'corsheaders',

    # GraphQL + JWT + Uploads
    'graphene_django',
    'graphql_jwt.refresh_token',       # si usas refresh tokens
    'graphene_file_upload.django',

    # Tu app
    'posts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # sirve static con WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── URLS & TEMPLATES ───────────────────────────────────────────────────────────
ROOT_URLCONF = 'gameforum_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gameforum_api.wsgi.application'

# ─── BASE DE DATOS ──────────────────────────────────────────────────────────────
# En local (DEBUG=True) y sin DATABASE_URL, usar SQLite:
if DEBUG and not os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # En producción o cuando tengo DATABASE_URL:
    DATABASE_URL = os.environ['DATABASE_URL']
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,  # Aiven exige TLS en producción
        )
    }

# ─── PASSWORDS & LOCALIZACIÓN ──────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# ─── STATIC & MEDIA ─────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── GRAPHENE & CORS ────────────────────────────────────────────────────────────
GRAPHENE = {
    'SCHEMA': 'posts.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
    'SCALARS': {
        'Upload': graphene_file_upload.scalars.Upload,
    }
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CORS_ALLOW_ALL_ORIGINS = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
