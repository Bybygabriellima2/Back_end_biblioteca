# Importando módulos necessários para gerenciamento de configurações e variáveis de ambiente
from pydantic_settings import BaseSettings  # Biblioteca para definir configurações com validação
import os  # Módulo para interagir com o sistema operacional
from dotenv import load_dotenv  # Função para carregar variáveis de ambiente de um arquivo .env

# Carrega variáveis de ambiente de um arquivo .env (se existir)
load_dotenv()

# Classe de configurações usando Pydantic BaseSettings
class Settings(BaseSettings):
    # URL de conexão para o banco de dados MySQL
    # Usa variável de ambiente ou um valor padrão se não definida
    # Formato: protocolo+driver://usuário:senha@host:porta/nome_do_banco
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:sua_senha@localhost:3306/biblioteca")
    
    # Chave secreta para assinatura de tokens
    # Usa variável de ambiente ou uma chave padrão (NÃO RECOMENDADO EM PRODUÇÃO)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "5f47ddd426fb93acefcceab2398643c9b274bac79c83b87cf9010c5469ffbf33")
    
    # Algoritmo de criptografia para tokens
    ALGORITHM: str = "HS256"
    
    # Tempo de expiração dos tokens de acesso em minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Cria uma instância das configurações
settings = Settings()