from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x7^vhv9+_)b$bel(_2*ifta=_9cb)7!o@o2weu6qx^o_zon==-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'https://laboratoriofigital.recife.pe.gov.br/desenvolvedores',
    'localhost',
    '127.0.0.1',
    '[::1]',  # Para IPv6
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'figital',

	'django_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# import pymysql
# pymysql.install_as_MySQLdb()  # Garante que Django use PyMySQL

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'db_dev_laboratoriofigital',
#         'USER': 'db_dev_laboratoriofigital',
#         'PASSWORD': 'edfjhsd@Hdhsb1sdjaHS2123f',
#         'HOST': 'caturrita.recife',
#         'PORT': '3306',
#         'OPTIONS': {
#             'sql_mode': 'STRICT_TRANS_TABLES',
#             'charset': 'utf8mb4',
#             'autocommit': True,
#             'init_command': "SET @@sql_mode = 'STRICT_TRANS_TABLES'",
#         }
#     }
# }

# Força Django a aceitar MySQL 5.7 como compatível
# from django.db.backends.mysql.base import DatabaseWrapper
# DatabaseWrapper.get_database_version = lambda self: (8, 0, 13)


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
import os

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "figital/static"),  # Diretório de arquivos estáticos durante o desenvolvimento
]


# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Diretório de arquivos estáticos durante a produção
STATIC_ROOT = os.path.join(BASE_DIR, "www", "staticfiles")

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'figital.Usuario'


# Configuração correta no settings.py
# LOGIN_REDIRECT_URL = '/meus-atendimentos/'  # Após login, redireciona para "Meus Atendimentos"
# LOGOUT_REDIRECT_URL = '/login/'  # Ou para qualquer outra página de sua escolha
LOGIN_URL = '/login/'  # URL que será usada para redirecionar usuários não autenticados

SESSION_COOKIE_AGE = 600  # 10 minutos (10 x 60 segundos)
SESSION_SAVE_EVERY_REQUEST = True # renova a validade a cada requisição
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Salva sessões no banco de dados

# Segurança em produção
   #SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True


CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

SECURE_SSL_REDIRECT = False  # Redireciona HTTP para HTTPS
SESSION_COOKIE_SECURE = True  # Apenas via HTTPS
CSRF_COOKIE_SECURE = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CSRF_TRUSTED_ORIGINS = [
    "https://laboratoriofigital.recife.pe.gov.br/desenvolvedores"
]
