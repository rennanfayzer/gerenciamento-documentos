# 1. Imagem base com Python
FROM python:3.11-slim

# 2. Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Instala dependências do sistema para WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgobject-2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia e instala as dependências do Python
COPY documentos/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o código do projeto para o diretório de trabalho
COPY ./documentos /app/

# 7. Expõe a porta que o Gunicorn vai usar
EXPOSE 8000

# 8. Comando para iniciar o servidor
CMD ["gunicorn", "documentos.wsgi:application", "--bind", "0.0.0.0:8000"]
