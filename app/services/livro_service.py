from app.repositories.livro_repository import LivroRepository
from app.schemas.livro_schema import LivroCreate
from app.exceptions import LivroNaoEncontradoException
import logging

# Configura um logger para registrar eventos e erros relacionados a livros
logger = logging.getLogger(__name__)

class LivroService:
    # Construtor do serviço de livros
    # Recebe um repositório de livros para realizar operações de banco de dados
    def __init__(self, livro_repository: LivroRepository):
        self.livro_repository = livro_repository

    # Método para criar um novo livro
    def create_livro(self, livro: LivroCreate):
        # Registra a criação de um novo livro
        logger.info(f"Criando novo livro: {livro.titulo}")
        # Delega a criação do livro para o repositório
        return self.livro_repository.create_livro(livro)

    # Método para buscar um livro pelo seu ID
    def get_livro_by_id(self, livro_id: int):
        # Busca o livro no repositório
        livro = self.livro_repository.get_livro_by_id(livro_id)
        
        # Verifica se o livro existe
        if not livro:
            # Registra tentativa de acessar livro inexistente
            logger.warning(f"Tentativa de acessar livro inexistente: {livro_id}")
            # Lança exceção para livro não encontrado
            raise LivroNaoEncontradoException()
        
        # Retorna o livro encontrado
        return livro

    # Método para buscar livros por autor
    def get_livros_by_autor(self, autor: str):
        # Registra a busca de livros por autor
        logger.info(f"Buscando livros do autor: {autor}")
        # Delega a busca para o repositório
        return self.livro_repository.get_livros_by_autor(autor)

    # Método para atualizar informações de um livro
    def update_livro(self, livro_id: int, livro_data: dict):
        # Verifica se o livro existe (lançará exceção se não existir)
        livro = self.get_livro_by_id(livro_id)
        
        # Registra a atualização do livro
        logger.info(f"Atualizando livro: {livro_id}")
        
        # Delega a atualização para o repositório
        return self.livro_repository.update_livro(livro_id, livro_data)

    # Método para deletar um livro
    def delete_livro(self, livro_id: int):
        # Verifica se o livro existe (lançará exceção se não existir)
        livro = self.get_livro_by_id(livro_id)
        
        # Registra a deleção do livro
        logger.info(f"Deletando livro: {livro_id}")
        
        # Delega a deleção para o repositório
        return self.livro_repository.delete_livro(livro_id)