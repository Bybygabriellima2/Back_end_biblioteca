# Importações necessárias do FastAPI para tratamento de exceções
from fastapi import HTTPException, status

# Classe base de exceção personalizada para a biblioteca
class BibliotecaException(HTTPException):
    """
    Exceção base para todas as exceções personalizadas da aplicação.
    Herda de HTTPException para integração direta com FastAPI.
    
    Parâmetros:
    - detail: Mensagem descritiva do erro
    - status_code: Código de status HTTP (padrão 400 Bad Request)
    """
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        # Chama o construtor da classe pai (HTTPException) com os parâmetros fornecidos
        super().__init__(status_code=status_code, detail=detail)

# Exceção para credenciais de autenticação inválidas
class CredenciaisInvalidasException(BibliotecaException):
    """
    Exceção lançada quando as credenciais de login são inválidas.
    Utiliza status 401 Unauthorized.
    """
    def __init__(self):
        # Chama o construtor da classe pai com mensagem e status específicos
        super().__init__(
            detail="Credenciais inválidas",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

# Exceção para livro não encontrado no acervo
class LivroNaoEncontradoException(BibliotecaException):
    """
    Exceção lançada quando um livro pesquisado não é encontrado.
    Utiliza status 404 Not Found.
    """
    def __init__(self):
        # Chama o construtor da classe pai com mensagem e status específicos
        super().__init__(
            detail="Livro não encontrado",
            status_code=status.HTTP_404_NOT_FOUND
        )

# Exceção para livro indisponível para empréstimo
class LivroIndisponivelException(BibliotecaException):
    """
    Exceção lançada quando um livro não está disponível para empréstimo.
    Utiliza status padrão 400 Bad Request.
    """
    def __init__(self):
        # Chama o construtor da classe pai com mensagem padrão
        super().__init__(
            detail="Livro não está disponível para empréstimo"
        )