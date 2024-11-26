# Importações necessárias para definir o modelo de Livro usando SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Cria a base declarativa para modelos SQLAlchemy
Base = declarative_base()

# Define a classe de modelo para Livro
class Livro(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "livros"

    # Definição das colunas da tabela
    
    # Coluna de ID (chave primária)
    # - primary_key=True: indica que é a chave primária
    # - index=True: cria um índice para melhorar performance de buscas
    id = Column(Integer, primary_key=True, index=True)

    # Coluna do título do livro
    # - Tipo String: armazena texto do título
    titulo = Column(String)

    # Coluna do autor do livro
    # - Tipo String: armazena texto do nome do autor
    autor = Column(String)

    # Coluna de disponibilidade do livro
    # - Tipo Boolean: indica se o livro está disponível para empréstimo
    # - default=True: por padrão, livros são considerados disponíveis ao serem cadastrados
    disponivel = Column(Boolean, default=True)