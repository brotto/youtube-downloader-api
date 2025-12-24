FROM python:3.11-slim

# Instala dependências do sistema necessárias para yt-dlp e ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Cria diretório para downloads
RUN mkdir -p /app/downloads

# Expõe a porta da aplicação
EXPOSE 5000

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV DOWNLOAD_DIR=/app/downloads
ENV PORT=5000

# Comando para executar a aplicação
CMD ["python", "app.py"]
