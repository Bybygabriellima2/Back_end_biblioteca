from sqlalchemy.orm import Session
from app.models.livro import Livro
from app.schemas.livro_schema import LivroCreate

class LivroRepository:
    # Método construtor que inicializa o repositório com uma sessão de banco de dados
    # Recebe uma sessão do SQLAlchemy como parâmetro para realizar operações no banco de dados
    def __init__(self, db: Session):
        self.db = db

    # Método para buscar um livro específico pelo seu ID
    # Retorna o primeiro livro que corresponde ao ID fornecido, ou None se nenhum livro for encontrado
    def get_livro_by_id(self, livro_id: int):
        return self.db.query(Livro).filter(Livro.id == livro_id).first()

    # Método para buscar todos os livros de um determinado autor
    # Retorna uma lista de livros escritos pelo autor especificado
    def get_livros_by_autor(self, autor: str):
        return self.db.query(Livro).filter(Livro.autor == autor).all()

    # Método para criar um novo livro no banco de dados
    # Converte o esquema de entrada para um modelo de banco de dados
    # Adiciona o novo livro à sessão, confirma a transação e retorna o livro criado
    def create_livro(self, livro: LivroCreate):
        # Converte o esquema de livro para um modelo de banco de dados
        db_livro = Livro(**livro.dict())
        # Adiciona o novo livro à sessão do banco de dados
        self.db.add(db_livro)
        # Confirma a transação, salvando as alterações no banco de dados
        self.db.commit()
        # Atualiza o objeto com os dados gerados pelo banco (como ID)
        self.db.refresh(db_livro)
        # Retorna o livro recem-criado
        return db_livro

    # Método para atualizar as informações de um livro existente
    # Atualiza o livro com o ID fornecido usando os dados passados
    # Confirma a transação e retorna o livro atualizado
    def update_livro(self, livro_id: int, livro_data: dict):
        # Atualiza o livro no banco de dados com os novos dados
        self.db.query(Livro).filter(Livro.id == livro_id).update(livro_data)
        # Confirma a transação
        self.db.commit()
        # Retorna o livro atualizado
        return self.get_livro_by_id(livro_id)

    # Método para excluir um livro do banco de dados
    # Busca o livro pelo ID, remove-o se encontrado e confirma a transação
    # Retorna o livro excluído ou None se nenhum livro for encontrado
    def delete_livro(self, livro_id: int):
        # Busca o livro pelo ID
        livro = self.get_livro_by_id(livro_id)
        # Se o livro existir, remove-o do banco de dados
        if livro:
            self.db.delete(livro)
            # Confirma a transação
            self.db.commit()
        # Retorna o livro excluído (ou None)
        return livro