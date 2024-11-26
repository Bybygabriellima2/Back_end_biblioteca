from app.repositories.emprestimo_repository import EmprestimoRepository
from app.repositories.livro_repository import LivroRepository
from app.exceptions import LivroIndisponivelException, LivroNaoEncontradoException
import logging

# Configura um logger para registrar eventos e erros relacionados a empréstimos
logger = logging.getLogger(__name__)

class EmprestimoService:
    # Construtor do serviço de empréstimos
    # Recebe repositórios de empréstimo e livro para realizar operações de banco de dados
    def __init__(
        self, 
        emprestimo_repository: EmprestimoRepository,
        livro_repository: LivroRepository
    ):
        self.emprestimo_repository = emprestimo_repository
        self.livro_repository = livro_repository

    # Método para criar um novo empréstimo
    def criar_emprestimo(self, usuario_id: int, livro_id: int):
        # Busca o livro pelo ID
        livro = self.livro_repository.get_livro_by_id(livro_id)
        
        # Verifica se o livro existe
        if not livro:
            # Registra tentativa de emprestar livro inexistente
            logger.warning(f"Tentativa de emprestar livro inexistente: {livro_id}")
            # Lança exceção para livro não encontrado
            raise LivroNaoEncontradoException()

        # Verifica se o livro está disponível para empréstimo
        if not livro.disponivel:
            # Registra tentativa de emprestar livro já emprestado
            logger.warning(f"Tentativa de emprestar livro indisponível: {livro_id}")
            # Lança exceção para livro indisponível
            raise LivroIndisponivelException()

        # Atualiza o status do livro para indisponível
        self.livro_repository.update_livro(livro_id, {"disponivel": False})

        # Cria o registro de empréstimo
        logger.info(f"Criando empréstimo do livro {livro_id} para usuário {usuario_id}")
        emprestimo = self.emprestimo_repository.create_emprestimo(usuario_id, livro_id)

        # Retorna o empréstimo criado
        return emprestimo

    # Método para finalizar um empréstimo
    def finalizar_emprestimo(self, emprestimo_id: int):
        # Finaliza o empréstimo no repositório
        emprestimo = self.emprestimo_repository.finalizar_emprestimo(emprestimo_id)
        
        # Se o empréstimo for encontrado e finalizado
        if emprestimo:
            # Atualiza o status do livro para disponível novamente
            self.livro_repository.update_livro(
                emprestimo.livro_id, 
                {"disponivel": True}
            )
            # Registra a finalização do empréstimo
            logger.info(f"Empréstimo {emprestimo_id} finalizado")
        
        # Retorna o empréstimo finalizado
        return emprestimo