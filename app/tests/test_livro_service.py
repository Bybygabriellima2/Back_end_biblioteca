import sys
import os
import pytest
from unittest.mock import Mock

# Adiciona o caminho do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.livro_service import LivroService
from app.schemas.livro_schema import LivroCreate
from app.exceptions import LivroNaoEncontradoException

def test_create_livro():
    # Preparação (Arrange)
    # Cria um mock do repositório de livros
    mock_repo = Mock()
    
    # Define o comportamento de retorno do método create_livro
    # Simula a criação de um livro com dados específicos
    mock_repo.create_livro.return_value = Mock(
        id=1, 
        titulo="Test Book",
        autor="Test Author",
        disponivel=True
    )
    
    # Instancia o serviço de livros com o repositório mockado
    service = LivroService(mock_repo)
    
    # Cria um objeto de esquema para criação de livro
    livro_data = LivroCreate(titulo="Test Book", autor="Test Author")

    # Execução (Act)
    # Chama o método de criação de livro do serviço
    result = service.create_livro(livro_data)

    # Verificação (Assert)
    # Verifica se os dados do livro criado estão corretos
    assert result.titulo == "Test Book"
    assert result.autor == "Test Author"
    
    # Verifica se o método create_livro do repositório foi chamado 
    # exatamente uma vez com os dados corretos
    mock_repo.create_livro.assert_called_once_with(livro_data)

def test_get_livro_by_id_not_found():
    # Preparação (Arrange)
    # Cria um mock do repositório de livros
    mock_repo = Mock()
    
    # Configura o método get_livro_by_id para retornar None
    # Simulando que nenhum livro foi encontrado
    mock_repo.get_livro_by_id.return_value = None
    
    # Instancia o serviço de livros com o repositório mockado
    service = LivroService(mock_repo)

    # Execução e Verificação (Act & Assert)
    # Verifica se uma exceção LivroNaoEncontradoException 
    # é lançada quando se tenta buscar um livro inexistente
    with pytest.raises(LivroNaoEncontradoException):
        service.get_livro_by_id(1)

def test_get_livro_by_id_success():
    # Preparação (Arrange)
    mock_repo = Mock()
    
    # Cria um mock de livro para simular um livro existente
    mock_livro = Mock(
        id=1, 
        titulo="Existing Book", 
        autor="Existing Author",
        disponivel=True
    )
    
    # Configura o repositório para retornar o livro mockado
    mock_repo.get_livro_by_id.return_value = mock_livro
    
    # Instancia o serviço de livros
    service = LivroService(mock_repo)

    # Execução (Act)
    # Busca o livro pelo ID
    result = service.get_livro_by_id(1)

    # Verificação (Assert)
    # Verifica se o livro retornado tem os dados corretos
    assert result.id == 1
    assert result.titulo == "Existing Book"
    assert result.autor == "Existing Author"
    
    # Verifica se o método do repositório foi chamado com o ID correto
    mock_repo.get_livro_by_id.assert_called_once_with(1)

def test_get_livros_by_autor():
    # Preparação (Arrange)
    mock_repo = Mock()
    
    # Cria uma lista mockada de livros de um autor
    mock_livros = [
        Mock(id=1, titulo="Book 1", autor="Test Author"),
        Mock(id=2, titulo="Book 2", autor="Test Author")
    ]
    
    # Configura o repositório para retornar a lista de livros
    mock_repo.get_livros_by_autor.return_value = mock_livros
    
    # Instancia o serviço de livros
    service = LivroService(mock_repo)

    # Execução (Act)
    # Busca livros de um autor específico
    result = service.get_livros_by_autor("Test Author")

    # Verificação (Assert)
    # Verifica se o número de livros retornados está correto
    assert len(result) == 2
    
    # Verifica se todos os livros são do autor correto
    assert all(livro.autor == "Test Author" for livro in result)
    
    # Verifica se o método do repositório foi chamado com o autor correto
    mock_repo.get_livros_by_autor.assert_called_once_with("Test Author")