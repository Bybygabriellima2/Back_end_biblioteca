from pydantic import BaseModel, EmailStr

# Esquema para criação de um novo usuário
# Utiliza Pydantic para validação de dados
class UserCreate(BaseModel):
    # Campo de e-mail que será validado como um endereço de e-mail válido
    # EmailStr garante que o e-mail tenha um formato correto
    email: EmailStr
    
    # Senha do usuário como string
    # Não há validações específicas de força de senha neste esquema
    password: str

# Esquema para autenticação de login de usuário
# Estrutura similar ao UserCreate, usado para validar credenciais de login
class UserLogin(BaseModel):
    # E-mail do usuário para autenticação
    email: EmailStr
    
    # Senha fornecida para verificação de login
    password: str

# Esquema para representar um token de autenticação
class Token(BaseModel):
    # Token de acesso gerado após autenticação bem-sucedida
    access_token: str
    
    # Tipo de token (geralmente "bearer")
    token_type: str

# Esquema para armazenar dados extras do token
class TokenData(BaseModel):
    # E-mail do usuário extraído do token
    # Permite valor None para lidar com tokens sem e-mail
    email: str | None = None