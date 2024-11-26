from pydantic import BaseModel

# Classe base para representar informações essenciais de um livro
# Contém os atributos compartilhados entre diferentes representações de livro
class LivroBase(BaseModel):
    # Título do livro
    # Campo obrigatório para identificação do livro
    titulo: str
    
    # Autor do livro
    # Campo obrigatório para identificar a autoria
    autor: str

# Esquema para criação de um novo livro
# Herda os campos básicos de LivroBase
# Neste caso, não adiciona novos campos, apenas serve como um marcador para criação
class LivroCreate(LivroBase):
    # Utiliza todos os campos de LivroBase (titulo e autor)
    # 'pass' indica que não são adicionados novos campos específicos para criação
    pass

# Esquema completo de um livro, incluindo informações adicionais
# Herda os campos básicos e adiciona campos específicos de um livro persistido
class Livro(LivroBase):
    # Identificador único do livro
    # Gerado pelo banco de dados ao persistir o registro
    id: int
    
    # Indica se o livro está disponível para empréstimo
    # Propriedade booleana que pode ser usada para controle de disponibilidade
    disponivel: bool

    # Configuração para compatibilidade com modelos ORM
    class Config:
        # Permite a criação do modelo a partir de objetos do banco de dados
        # Facilita a conversão de modelos SQLAlchemy para esquemas Pydantic
        orm_mode = True