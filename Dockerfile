# Usa uma imagem oficial e leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código para dentro do contêiner
COPY . .

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Comando para iniciar o servidor
CMD ["python", "run.py"]