# Usa uma imagem oficial do Python como base
FROM python:3.10

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    && apt-get clean

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para dentro do container
COPY requirements.txt /app/requirements.txt

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o container
COPY . /app

# Expõe a porta onde o Gradio/Flask rodará (se necessário)
EXPOSE 7860

# Comando para rodar o aplicativo
CMD ["python", "app.py"]

