# Use uma imagem base Python oficial. Escolha a versão que você usou localmente.
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
# e instala as dependências. Usamos --no-cache-dir para economizar espaço na imagem.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da sua aplicação para o diretório de trabalho
COPY . .

# Comando para iniciar a aplicação Uvicorn quando o contêiner for executado.
# 'main' é o nome do seu arquivo Python (main.py)
# 'app' é a instância do FastAPI (app = FastAPI())
# '--host 0.0.0.0' faz com que o Uvicorn escute em todas as interfaces de rede dentro do contêiner.
# '--port $PORT' usa a variável de ambiente $PORT que o Cloud Run injeta.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
