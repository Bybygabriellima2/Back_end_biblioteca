# Importações necessárias para configuração do banco de dados
from sqlalchemy import create_engine  # Cria o motor de conexão com o banco de dados
from sqlalchemy.ext.declarative import declarative_base  # Classe base para modelos ORM
from sqlalchemy.orm import sessionmaker  # Cria sessões de banco de dados
from app.config import settings  # Importa as configurações da aplicação
import pymysql  # Driver MySQL para SQLAlchemy

# Instala o pymysql como adaptador MySQL para o SQLAlchemy
pymysql.install_as_MySQLdb()

# Criação do motor de conexão com o banco de dados
# Configurações detalhadas do pool de conexões:
engine = create_engine(
    settings.DATABASE_URL,  # URL de conexão definida nas configurações
    pool_size=5,            # Número de conexões mantidas no pool
    max_overflow=10,        # Número máximo de conexões que podem ser criadas além do pool base
    pool_timeout=30,        # Tempo máximo de espera para obter uma conexão do pool
    pool_recycle=1800,      # Reconecta conexões após 30 minutos (1800 segundos)
    echo=False              # Desativa o log de SQL (usar True apenas para depuração)
)

# Cria uma fábrica de sessões do banco de dados
SessionLocal = sessionmaker(
    autocommit=False,  # Desativa o autocommit (commits manuais)
    autoflush=False,   # Desativa o autoflush (flush manual das alterações)
    bind=engine        # Vincula a sessão ao motor de conexão
)

# Cria uma classe base para modelos ORM
Base = declarative_base()

# Função para gerenciar sessões de banco de dados
def get_db():
    """
    Gerenciador de contexto para sessões de banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db  # Fornece a sessão para uso
    finally:
        db.close()  # Fecha a sessão após o uso

# Função para inicializar o banco de dados
def init_db():
    """
    Cria todas as tabelas definidas nos modelos
    baseadas na classe Base
    """
    Base.metadata.create_all(bind=engine)