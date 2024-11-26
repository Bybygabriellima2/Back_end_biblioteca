from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import UserCreate, UserLogin, TokenData
from app.exceptions import CredenciaisInvalidasException
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def create_user(self, user: UserCreate):
        logger.info(f"Criando novo usuário com email: {user.email}")
        return self.auth_repository.create_user(user)

    def authenticate_user(self, user_login: UserLogin):
    # Altere esta linha
        user = self.auth_repository.get_user_by_email(user_login.username)
        if not user or not self.auth_repository.verify_password(
            user_login.password, user.hashed_password
        ):
            logger.warning(f"Tentativa de login mal sucedida para email: {user_login.username}")
            raise CredenciaisInvalidasException()
        
        logger.info(f"Login bem sucedido para usuário: {user_login.username}")
        return user

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise CredenciaisInvalidasException()
            return TokenData(email=email)
        except JWTError:
            raise CredenciaisInvalidasException()