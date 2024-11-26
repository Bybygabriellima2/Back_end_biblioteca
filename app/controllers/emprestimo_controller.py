# Importações necessárias para criar o controlador de empréstimos
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.emprestimo_service import EmprestimoService
from app.repositories.emprestimo_repository import EmprestimoRepository
from app.repositories.livro_repository import LivroRepository
from app.schemas.emprestimo_schema import EmprestimoCreate, Emprestimo
from app.auth import get_current_user
import logging

# Cria um roteador do FastAPI para definir rotas de empréstimos
router = APIRouter()

# Configura o logger para registrar eventos e erros
logger = logging.getLogger(__name__)  # Correção no nome do logger

# Função para obter o serviço de empréstimo com injeção de dependência do banco de dados
def get_emprestimo_service(db: Session = Depends(get_db)):
    return EmprestimoService(
        EmprestimoRepository(db),
        LivroRepository(db)
    )

# Rota para criar um novo empréstimo
@router.post("/emprestimos/", response_model=Emprestimo)
async def create_emprestimo(
    # Recebe os dados do empréstimo a ser criado
    emprestimo: EmprestimoCreate,
    
    # Obtém o usuário atualmente autenticado
    current_user: dict = Depends(get_current_user),
    
    # Injeta o serviço de empréstimo como dependência
    emprestimo_service: EmprestimoService = Depends(get_emprestimo_service)
):
    try:
        # Registra log da tentativa de empréstimo
        logger.info(f"Usuário {current_user.id} tentando emprestar livro {emprestimo.livro_id}")
        
        # Chama o serviço para criar o empréstimo
        # Passa o ID do usuário atual e o ID do livro
        emprestimo_criado = emprestimo_service.criar_emprestimo(
            usuario_id=current_user.id,  # Passando o ID do usuário atual
            livro_id=emprestimo.livro_id
        )
        
        # Registra log de sucesso na criação do empréstimo
        logger.info(f"Empréstimo criado com sucesso: {emprestimo_criado.id}")
        
        # Retorna o empréstimo criado
        return emprestimo_criado
    
    except Exception as e:
        # Registra log de erro caso ocorra algum problema
        logger.error(f"Erro ao criar empréstimo: {str(e)}")
        
        # Lança uma exceção HTTP com detalhes do erro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar empréstimo: {str(e)}"
        )