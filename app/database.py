"""
database.py
-----------
Aqui a gente configura a conexão com o banco de dados SQLite.

O SQLite é um banco de dados que vive dentro de um ÚNICO arquivo no seu
computador (nesse caso, "salas.db"). Não precisa instalar servidor
nenhum -- por isso é ótimo pra aprender e pra projetos pequenos/médios
como o de vocês.
"""

from sqlmodel import SQLModel, create_engine, Session

# "sqlite:///salas.db" significa: "use o SQLite, e salve os dados
# no arquivo salas.db, na mesma pasta do projeto".
DATABASE_URL = "sqlite:///salas.db"

# O "engine" é o objeto que sabe como conversar com o banco.
# connect_args é uma configuração específica que o SQLite exige quando
# usado com FastAPI (permite que o banco seja acessado por threads
# diferentes, o que o Uvicorn faz internamente).
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def criar_banco_e_tabelas():
    """
    Olha para todas as classes que herdam de SQLModel com table=True
    (no nosso caso, só a "Sala") e cria as tabelas correspondentes
    no banco, CASO elas ainda não existam.

    Chamamos essa função uma vez, quando a API sobe (ver main.py).
    """
    SQLModel.metadata.create_all(engine)


def obter_sessao():
    """
    Uma "Session" é como uma conversa temporária com o banco: você abre,
    faz as operações (criar, buscar, atualizar, deletar) e fecha.

    Essa função é o que chamamos de "dependency" no FastAPI: o próprio
    framework vai chamá-la automaticamente pra cada requisição, abrir
    uma sessão, entregar pra função da rota usar, e fechar sozinha
    no final -- sem vocês precisarem se preocupar em fechar manualmente.
    """
    with Session(engine) as sessao:
        yield sessao
