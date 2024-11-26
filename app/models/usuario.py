# Importações necessárias para definir o modelo de Usuário usando SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Cria a base declarativa para modelos SQLAlchemy
Base = declarative_base()

# Define a classe de modelo para Usuário
class Usuario(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "usuarios"

    # Definição das colunas da tabela
    
    # Coluna de ID (chave primária)
    # - primary_key=True: indica que é a chave primária
    # - index=True: cria um índice para melhorar performance de buscas
    id = Column(Integer, primary_key=True, index=True)

    # Coluna de email do usuário
    # - unique=True: garante que não haja emails duplicados
    # - index=True: cria um índice para melhorar performance de buscas por email
    email = Column(String, unique=True, index=True)

    # Coluna de senha (hash)
    # - Armazena a senha criptografada, nunca a senha em texto plano
    hashed_password = Column(String)

    # Coluna para definir privilégios de administrador
    # - default=False: por padrão, usuários não são administradores
    is_admin = Column(Boolean, default=False)