# Importações necessárias para criar o controlador de livros
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.livro_service import LivroService
from app.repositories.livro_repository import LivroRepository
from app.schemas.livro_schema import LivroCreate, Livro
from app.auth import get_current_user
import logging

# Cria um roteador do FastAPI para definir rotas de livros
router = APIRouter()

# Configura o logger para registrar eventos e erros
logger = logging.getLogger(__name__)

# Função para obter o serviço de livro com injeção de dependência do banco de dados
def get_livro_service(db: Session = Depends(get_db)):
    return LivroService(LivroRepository(db))

# Rota para criar um novo livro
@router.post("/livros/", response_model=Livro)
async def create_livro(
    # Recebe os dados do livro a ser criado
    livro: LivroCreate,
    
    # Obtém o usuário atualmente autenticado
    current_user: dict = Depends(get_current_user),
    
    # Injeta o serviço de livro como dependência
    livro_service: LivroService = Depends(get_livro_service)
):
    try:
        # Chama o serviço para criar o livro
        return livro_service.create_livro(livro)
    except Exception as e:
        # Registra log de erro caso ocorra algum problema
        logger.error(f"Erro ao criar livro: {str(e)}")
        
        # Lança uma exceção HTTP com detalhes do erro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar livro"
        )

# Rota para buscar livros por autor
@router.get("/livros/autor/{autor}", response_model=List[Livro])
async def get_livros_by_autor(
    # Recebe o nome do autor como parâmetro de rota
    autor: str,
    
    # Obtém o usuário atualmente autenticado
    current_user: dict = Depends(get_current_user),
    
    # Injeta o serviço de livro como dependência
    livro_service: LivroService = Depends(get_livro_service)
):
    # Chama o serviço para buscar livros por autor
    return livro_service.get_livros_by_autor(autor)

# Rota para atualizar um livro existente
@router.put("/livros/{livro_id}", response_model=Livro)
async def update_livro(
    # Recebe o ID do livro a ser atualizado
    livro_id: int,
    
    # Recebe os novos dados do livro
    livro: LivroCreate,
    
    # Obtém o usuário atualmente autenticado
    current_user: dict = Depends(get_current_user),
    
    # Injeta o serviço de livro como dependência
    livro_service: LivroService = Depends(get_livro_service)
):
    try:
        # Chama o serviço para atualizar o livro
        return livro_service.update_livro(livro_id, livro.dict())
    except Exception as e:
        # Registra log de erro caso ocorra algum problema
        logger.error(f"Erro ao atualizar livro: {str(e)}")
        
        # Lança uma exceção HTTP com detalhes do erro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar livro"
        )

# Rota para deletar um livro
@router.delete("/livros/{livro_id}", response_model=Livro)
async def delete_livro(
    # Recebe o ID do livro a ser deletado
    livro_id: int,
    
    # Obtém o usuário atualmente autenticado
    current_user: dict = Depends(get_current_user),
    
    # Injeta o serviço de livro como dependência
    livro_service: LivroService = Depends(get_livro_service)
):
    # Chama o serviço para deletar o livro
    return livro_service.delete_livro(livro_id)