"""
models.py
---------
Aqui definimos como a tabela "Sala" vai existir dentro do banco de dados.

Estamos usando a biblioteca SQLModel, que junta duas coisas em uma só classe:

1) Validação de dados (o que o Pydantic faz) -> garante que "capacidade"
   seja um número, que "nome" seja um texto, etc.
2) Mapeamento para o banco (o que o SQLAlchemy faz) -> transforma essa
   classe Python em uma tabela SQL de verdade.

Ou seja: uma classe só = o "formato" dos dados E a tabela do banco.
"""

from pyclbr import Class
from typing import Optional
from sqlmodel import SQLModel, Field


class Sala(SQLModel, table=True):
    """
    Cada atributo abaixo vira uma COLUNA da tabela "sala" no banco.
    Cada instância dessa classe vira uma LINHA da tabela.
    """

    # id: é a chave primária (identificador único de cada sala).
    # Optional[int] porque, ao CRIAR uma sala, ainda não sabemos o id
    # (quem gera é o próprio banco, automaticamente).
    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str
    descricao: str
    capacidade: int
    preco: float

    # Toda sala nasce ativa (True). A locadora pode desativar depois,
    # sem precisar apagar o registro do banco.
    ativa: bool = Field(default=True)


# ---------------------------------------------------------------------
# Por que criar classes SEPARADAS para entrada e saída de dados?
# ---------------------------------------------------------------------
# A classe "Sala" acima tem o campo "id". Mas quando o cliente vai
# CRIAR uma sala, ele não deve enviar um id (quem decide o id é o banco).
# Por isso criamos uma classe "SalaCreate" só com os campos que o
# usuário realmente deve preencher.
#
# Isso é uma prática comum em APIs: separar o "formato de entrada"
# do "formato de saída/tabela".

class SalaCreate(SQLModel):
    nome: str
    descricao: str
    capacidade: int
    preco: float


class SalaUpdate(SQLModel):
    """
    Todos os campos são Optional aqui porque, ao ATUALIZAR uma sala,
    o usuário pode querer mudar só o preço, por exemplo, sem precisar
    reenviar nome, descrição e capacidade de novo.
    """
    nome: Optional[str] = None
    descricao: Optional[str] = None
    capacidade: Optional[int] = None
    preco: Optional[float] = None
    ativa: Optional[bool] = None



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    cpf: str

class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    cpf: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    cpf: Optional[str] = None