# Importações necessárias para definir o modelo de Empréstimo usando SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Cria a base declarativa para modelos SQLAlchemy
Base = declarative_base()

# Define a classe de modelo para Empréstimo
class Emprestimo(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "emprestimos"  # Correção: __tablename__

    # Definição das colunas da tabela
    
    # Coluna de ID (chave primária)
    # - primary_key=True: indica que é a chave primária
    # - index=True: cria um índice para melhorar performance de buscas
    id = Column(Integer, primary_key=True, index=True)

    # Coluna de ID do usuário (chave estrangeira referenciando a tabela de usuários)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Coluna de ID do livro (chave estrangeira referenciando a tabela de livros)
    livro_id = Column(Integer, ForeignKey("livros.id"))

    # Coluna de data do empréstimo
    # - default=datetime.utcnow: define a data atual automaticamente quando criado
    data_emprestimo = Column(DateTime, default=datetime.utcnow)

    # Coluna de data de devolução
    # - nullable=True: permite que seja nulo (livro ainda não devolvido)
    data_devolucao = Column(DateTime, nullable=True)

    # Relacionamentos (comentado, mas pode ser usado para facilitar consultas)
    # usuario = relationship("Usuario", back_populates="emprestimos")