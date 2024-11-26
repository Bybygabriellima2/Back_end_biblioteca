from pydantic import BaseModel
from datetime import datetime

# Esquema para criação de um novo empréstimo
# Usado para validar os dados de entrada ao registrar um novo empréstimo
class EmprestimoCreate(BaseModel):
    # ID do livro a ser emprestado
    # Representa qual livro está sendo emprestado
    livro_id: int

# Esquema completo de um empréstimo
# Representa todos os detalhes de um empréstimo existente no banco de dados
class Emprestimo(BaseModel):
    # Identificador único do empréstimo
    id: int
    
    # ID do usuário que está fazendo o empréstimo
    usuario_id: int
    
    # ID do livro sendo emprestado
    livro_id: int
    
    # Data e hora em que o empréstimo foi realizado
    # Registra o momento exato do empréstimo
    data_emprestimo: datetime
    
    # Data e hora da devolução do livro
    # Permite valor None para empréstimos ainda não devolvidos
    data_devolucao: datetime | None

    # Configuração para compatibilidade com modelos ORM (Object-Relational Mapping)
    class Config:
        # Permite a criação do modelo a partir de objetos do banco de dados
        # Facilita a conversão de modelos SQLAlchemy para esquemas Pydantic
        orm_mode = True