from pathlib import Path
import os
import dj_database_url

# 🔹 Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔹 Configurações básicas
DEBUG = os.getenv("DEBUG", "1") == "1"
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")

ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1", "0.0.0.0"]


# 🔹 Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do projeto
    'order',
    'product',

    # Swagger / DRF
    'rest_framework',
    'drf_yasg',
]

# 🔹 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔹 Arquivos de rotas
ROOT_URLCONF = 'book.urls'

# 🔹 Templates
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

# 🔹 WSGI
WSGI_APPLICATION = 'book.wsgi.application'

# 🔹 Banco de dados
if os.getenv("USE_SQLITE", "false").lower() == "true":
    print("⚙️  Usando banco SQLite (modo autônomo)")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    print("🗄️  Usando banco PostgreSQL (modo Compose)")
    DATABASES = {
        "default": dj_database_url.config(
            default=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
            conn_max_age=600,
        )
    }

# 🔹 Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔹 Campo padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
