# Importando módulos necessários do FastAPI e SQLAlchemy para autenticação e gerenciamento de banco de dados
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.repositories.auth_repository import AuthRepository

# Configurando um esquema de autenticação OAuth2 para tokens, especificando a URL de obtenção de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função assíncrona para obter o usuário atual autenticado
async def get_current_user(
    # Dependência para extrair o token do cabeçalho de autorização
    token: str = Depends(oauth2_scheme),
    # Dependência para obter uma sessão de banco de dados
    db: Session = Depends(get_db)
):
    # Criando uma instância do serviço de autenticação com o repositório de autenticação
    auth_service = AuthService(AuthRepository(db))
    
    # Verificando a validade do token e extraindo os dados do token
    token_data = auth_service.verify_token(token)
    
    # Buscando o usuário no banco de dados usando o email extraído do token
    user = auth_service.auth_repository.get_user_by_email(token_data.email)
    
    # Verificando se o usuário existe
    if user is None:
        # Se o usuário não for encontrado, lança uma exceção de não autorizado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inválido"
        )
    
    # Retorna o usuário autenticado
    return user