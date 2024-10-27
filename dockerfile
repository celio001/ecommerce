# Use uma imagem do Python com uma versão específica
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos
COPY requirements.txt /app/

# Atualiza a lista de pacotes e instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . /app/

# Expõe a porta em que a aplicação irá rodar
EXPOSE 3000

# Comando para executar a aplicação
CMD ["python", "run.py"]
