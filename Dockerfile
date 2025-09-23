# Imagem base
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* /app/

# Instalar Poetry e dependências
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copiar o restante do projeto
COPY . /app

# Expor porta do Django
EXPOSE 8000

# Comando para rodar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


