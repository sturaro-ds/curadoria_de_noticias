# Usa uma imagem oficial com Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade openai

# Copia o restante da aplicação
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 8000

# Define a variável de ambiente para produção
ENV FLASK_APP=app-noticias.py

# Comando para iniciar o Flask
CMD ["python", "app-noticias.py"]