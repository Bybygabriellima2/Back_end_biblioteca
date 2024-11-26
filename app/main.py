# Importações necessárias do FastAPI e da aplicação
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.controllers import auth_controller, livro_controller, emprestimo_controller  # Importando os controladores
import logging  # Módulo para configuração de logs

# Configuração de logging (registros de eventos)
logging.basicConfig(
    level=logging.INFO,  # Nível de log: informações gerais
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Formato do log
    # Exemplo de saída: "2024-01-15 10:30:45 - nome_do_logger - INFO - Mensagem de log"
)

# Criação das tabelas no banco de dados
# Garante que todas as tabelas definidas nos modelos sejam criadas
Base.metadata.create_all(bind=engine)

# Criação da instância principal do FastAPI
app = FastAPI(
    title="Biblioteca Digital API",  # Título da API
    description="API para gerenciamento de biblioteca digital",  # Descrição
    version="1.0.0"  # Versão da API
)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite requisições de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,  # Permite cookies e autenticação
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Incluindo os routers (roteadores) da aplicação
# Cada controlador define um conjunto de rotas relacionadas
app.include_router(auth_controller.router, tags=["auth"])  # Rotas de autenticação
app.include_router(livro_controller.router, tags=["livros"])  # Rotas de livros
app.include_router(emprestimo_controller.router, tags=["emprestimos"])  # Rotas de empréstimos

# Rota raiz da API
@app.get("/")
async def root():
    """
    Endpoint de boas-vindas para a API
    Retorna uma mensagem simples de boas-vindas
    """
    return {"message": "Bem-vindo à API da Biblioteca Digital"}