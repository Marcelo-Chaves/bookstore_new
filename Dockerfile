# Imagem base
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências de sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências do Poetry
COPY pyproject.toml poetry.lock* /app/

# Instalar Poetry
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

# Instalar dependências do projeto
RUN poetry install --with dev --no-root --no-interaction --no-ansi

# Copiar o restante do projeto
COPY . /app

# Copiar script wait-for-it (para uso com Docker Compose)
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Expor porta do Django
EXPOSE 8000

# Variável padrão para usar SQLite (modo autônomo)
ENV USE_SQLITE=true

# Comando de inicialização:
# - Se USE_SQLITE=true → roda direto com SQLite (modo autônomo)
# - Se USE_SQLITE=false → espera o PostgreSQL (modo Compose)
CMD ["sh", "-c", "\
if [ \"$USE_SQLITE\" = \"true\" ]; then \
    echo '✅ Executando com SQLite (modo autônomo)...'; \
    python manage.py migrate && python manage.py runserver 0.0.0.0:8000; \
else \
    echo '⏳ Aguardando PostgreSQL (modo Compose)...'; \
    ./wait-for-it.sh db:5432 --timeout=30 --strict -- \
    python manage.py migrate && python manage.py runserver 0.0.0.0:8000; \
fi"]
