FROM python:3.10

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    && apt-get clean

# Definir variáveis de ambiente
ENV PATH="/usr/bin:$PATH"

# Instalar bibliotecas Python
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do app
COPY . /app

# Rodar o aplicativo
CMD ["python", "app.py"]
