# Imagem base
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para compilar pacotes Python
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

# Instalar dependências do projeto (sem instalar o próprio pacote, só dependências)
RUN poetry install --with dev --no-root --no-interaction --no-ansi

# Copiar restante do projeto
COPY . /app

# Script wait-for-it
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Expor porta do Django
EXPOSE 8000

# Comando para rodar o servidor
CMD ["./wait-for-it.sh", "db:5432", "--timeout=30", "--strict", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
