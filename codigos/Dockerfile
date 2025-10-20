# Dockerfile para o Projeto Figital
# ----------------------------------

# Etapa 1: Imagem Base
# Usamos uma imagem oficial do Python, leve e otimizada (slim).
FROM python:3.11.5-slim

# --- Variáveis de Ambiente ---
# Garante que o output do python seja enviado direto para o terminal, facilitando o debug.
ENV PYTHONUNBUFFERED 1
# Define o encoding padrão para UTF-8, evitando problemas com caracteres especiais.
ENV PYTHONIOENCODING=UTF-8

# --- Instalação de Dependências do Sistema ---
# Atualiza os pacotes e instala bibliotecas necessárias para compilar algumas dependências Python.
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    # Limpa o cache do apt para reduzir o tamanho final da imagem.
    && rm -rf /var/lib/apt/lists/*

# --- Configuração do Projeto ---
# Define o diretório de trabalho principal DENTRO do container.
WORKDIR /app

# Copia a pasta 'www' (que contém seu código Django) para dentro do diretório '/app' no container.
COPY ./www /app

# --- Instalação das Dependências Python ---
# Instala as bibliotecas Python listadas no seu arquivo requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# --- Banco de Dados e Arquivos Estáticos ---
# Executa o comando para coletar todos os arquivos estáticos em um único diretório.
RUN python manage.py collectstatic --noinput

# Executa as migrações para criar as tabelas no banco de dados.
RUN python manage.py migrate --noinput

# --- Execução da Aplicação ---
# O comando que será executado quando o container iniciar.
# Inicia o servidor Gunicorn para rodar a aplicação em produção.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]