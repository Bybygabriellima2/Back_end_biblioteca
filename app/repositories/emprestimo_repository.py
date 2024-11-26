# Importações necessárias para o repositório de empréstimos
from sqlalchemy.orm import Session
from app.models.emprestimo import Emprestimo
from datetime import datetime

# Classe de repositório para operações de empréstimo
class EmprestimoRepository:
    # Construtor que recebe a sessão do banco de dados
    def __init__(self, db: Session):
        # Armazena a sessão do banco de dados para uso nos métodos
        self.db = db

    # Método para criar um novo empréstimo
    def create_emprestimo(self, usuario_id: int, livro_id: int):
        # Cria uma nova instância de Emprestimo
        # - usuario_id: ID do usuário que está emprestando
        # - livro_id: ID do livro sendo emprestado
        # - data_emprestimo: data atual em UTC
        db_emprestimo = Emprestimo(
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_emprestimo=datetime.utcnow()
        )

        # Operações de persistência no banco de dados
        # - add(): prepara o objeto para inserção
        self.db.add(db_emprestimo)
        # - commit(): salva as mudanças no banco de dados
        self.db.commit()
        # - refresh(): recarrega o objeto com dados do banco (como ID gerado)
        self.db.refresh(db_emprestimo)

        # Retorna o empréstimo recem-criado
        return db_emprestimo

    # Método para buscar todos os empréstimos de um usuário
    def get_emprestimos_by_usuario(self, usuario_id: int):
        # Consulta o banco de dados para encontrar empréstimos do usuário
        # - filter(): aplica condição de busca pelo ID do usuário
        # - all(): retorna todos os resultados encontrados
        return self.db.query(Emprestimo).filter(
            Emprestimo.usuario_id == usuario_id
        ).all()

    # Método para finalizar (devolver) um empréstimo
    def finalizar_emprestimo(self, emprestimo_id: int):
        # Busca o empréstimo específico pelo ID
        emprestimo = self.db.query(Emprestimo).filter(
            Emprestimo.id == emprestimo_id
        ).first()
        
        # Verifica se o empréstimo existe
        if emprestimo:
            # Define a data de devolução como data atual em UTC
            emprestimo.data_devolucao = datetime.utcnow()
            
            # Salva as alterações no banco de dados
            self.db.commit()
            
            # Recarrega o objeto para garantir sincronização
            self.db.refresh(emprestimo)
        
        # Retorna o empréstimo (pode ser None se não encontrado)
        return emprestimo