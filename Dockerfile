FROM python:3.10

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-por \
    libgl1

# Definir variável de ambiente para o Tesseract encontrar os idiomas
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Rodar o aplicativo
CMD ["python", "app.py"]
