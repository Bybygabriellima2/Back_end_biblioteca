# Importações de bibliotecas necessárias para criar a API de autenticação
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import UserCreate, Token
import logging

# Cria um roteador do FastAPI para definir rotas de autenticação
router = APIRouter()

# Configura o esquema OAuth2 para autenticação com token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configura o logger para registrar eventos e erros
logger = logging.getLogger(__name__)

# Função para obter o serviço de autenticação com injeção de dependência do banco de dados
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(AuthRepository(db))

# Rota para registrar um novo usuário
@router.post("/register", response_model=Token)
async def register(
    # Recebe os dados do usuário a ser criado
    user: UserCreate, 
    # Injeta o serviço de autenticação como dependência
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        # Tenta criar o usuário usando o serviço de autenticação
        user = auth_service.create_user(user)
        
        # Gera um token de acesso para o usuário recem-criado
        access_token = auth_service.create_access_token(
            data={"sub": user.email}
        )
        
        # Retorna o token de acesso
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        # Registra qualquer erro que ocorra durante o registro
        logger.error(f"Erro ao registrar usuário: {str(e)}")
        
        # Lança uma exceção HTTP em caso de falha no registro
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao registrar usuário"
        )

# Rota para autenticação de usuário (login)
@router.post("/token", response_model=Token)
async def login(
    # Utiliza o formulário padrão do OAuth2 para receber credenciais
    form_data: OAuth2PasswordRequestForm = Depends(),
    # Injeta o serviço de autenticação como dependência
    auth_service: AuthService = Depends(get_auth_service)
):
    # Autentica o usuário usando o serviço de autenticação
    user = auth_service.authenticate_user(form_data)
    
    # Gera um token de acesso para o usuário autenticado
    access_token = auth_service.create_access_token(
        data={"sub": user.email} 
    )
    
    # Retorna o token de acesso
    return {"access_token": access_token, "token_type": "bearer"}