# Imagem base
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos de dependências do Poetry
COPY pyproject.toml poetry.lock* /app/

# Instalar Poetry e dependências
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copiar restante do projeto
COPY . /app

# Copiar script wait-for-it
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Expor porta do Django
EXPOSE 8000

# Comando para rodar o servidor
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
