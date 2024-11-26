# Importações necessárias para o repositório de autenticação
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.auth_schema import UserCreate
from passlib.context import CryptContext

# Configuração do contexto de hash de senha
# - Usa bcrypt como algoritmo de hash
# - deprecated="auto": lida com versões antigas de hash se necessário
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Classe de repositório para operações de autenticação
class AuthRepository:
    # Construtor que recebe a sessão do banco de dados
    def __init__(self, db: Session):
        # Armazena a sessão do banco de dados para uso nos métodos
        self.db = db

    # Método para buscar usuário por e-mail
    def get_user_by_email(self, email: str):
        # Consulta o banco de dados para encontrar usuário com o e-mail específico
        # - filter(): aplica condição de busca
        # - first(): retorna o primeiro resultado ou None
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    # Método para criar novo usuário
    def create_user(self, user: UserCreate):
        # Hash da senha fornecida
        # - Converte senha em texto plano para uma versão segura hasheada
        hashed_password = pwd_context.hash(user.password)

        # Cria instância do modelo de usuário
        # - Usa e-mail do schema de criação
        # - Usa senha hasheada, nunca a senha em texto plano
        db_user = Usuario(email=user.email, hashed_password=hashed_password)

        # Operações de persistência no banco de dados
        # - add(): prepara o objeto para inserção
        self.db.add(db_user)
        # - commit(): salva as mudanças no banco de dados
        self.db.commit()
        # - refresh(): recarrega o objeto com dados do banco (como ID gerado)
        self.db.refresh(db_user)

        # Retorna o usuário recem-criado
        return db_user

    # Método para verificar senha
    def verify_password(self, plain_password: str, hashed_password: str):
        # Verifica se a senha em texto plano corresponde ao hash armazenado
        # - Usa o contexto de hash para comparação segura
        return pwd_context.verify(plain_password, hashed_password)