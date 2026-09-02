"""
main.py
-------
Este é o arquivo principal da API. Aqui vivem as ROTAS: os endereços
que o Bubble (ou o Postman, ou o navegador) vai chamar para criar,
listar, atualizar e deletar salas.

Como rodar:
    1. pip install -r requirements.txt
    2. uvicorn main:app --reload
    3. Abra http://127.0.0.1:8000/docs no navegador

Esse /docs é uma tela AUTOMÁTICA que o FastAPI gera, onde dá pra
testar cada rota clicando em botões -- sem precisar nem do Postman
pra começar a testar.
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select    

from app.database import criar_banco_e_tabelas, obter_sessao
from app.models import Sala, SalaCreate, SalaUpdate, User, UserCreate, UserUpdate


# "app" é a instância principal da nossa API. É nela que penduramos
# todas as rotas abaixo.
app = FastAPI()


@app.on_event("startup")
def ao_iniciar():
    """
    Esse decorador (@app.on_event("startup")) diz ao FastAPI:
    "antes de começar a aceitar requisições, rode esta função uma vez".
    Usamos isso pra garantir que o arquivo salas.db e a tabela existam.
    """
    criar_banco_e_tabelas()


# CREATE - criar uma nova sala

# @app.post(...) diz: "essa função responde a requisições HTTP do tipo
# POST, no endereço /salas". POST é o verbo usado, por convenção,
# para CRIAR alguma coisa nova.
#
# "sala: SalaCreate" diz ao FastAPI: "espere um JSON no corpo da
# requisição, no formato da classe SalaCreate (nome, descricao,
# capacidade, preco) -- e valide isso automaticamente pra mim".
#
# "sessao: Session = Depends(obter_sessao)" é o FastAPI perguntando
# lá na database.py por uma sessão de banco pronta pra usar.

@app.post("/salas", response_model=Sala)
def criar_sala(sala: SalaCreate, sessao: Session = Depends(obter_sessao)):
    # Transforma o dado de entrada (SalaCreate) em uma Sala de verdade,
    # que é o formato que sabe virar linha de tabela.
    nova_sala = Sala.model_validate(sala)

    sessao.add(nova_sala)      # prepara a sala pra ser salva
    sessao.commit()            # de fato grava no banco
    sessao.refresh(nova_sala)  # atualiza "nova_sala" com o id gerado pelo banco

    return nova_sala


# READ - listar todas as salas

# @app.get diz: "responde a requisições GET", que é o verbo usado por
# convenção pra BUSCAR dados (sem alterar nada no banco).

@app.get("/salas", response_model=List[Sala])
def listar_salas(sessao: Session = Depends(obter_sessao)):
    # select(Sala) monta a instrução "SELECT * FROM sala" por baixo dos panos.
    salas = sessao.exec(select(Sala)).all()
    return salas


# READ - buscar UMA sala específica pelo id

# "{sala_id}" na rota é um parâmetro dinâmico: /salas/1, /salas/2, etc.
# O FastAPI já entende que sala_id deve ser um número (int), pela
# anotação de tipo que colocamos no parâmetro da função.

@app.get("/salas/{sala_id}", response_model=Sala)
def buscar_sala(sala_id: int, sessao: Session = Depends(obter_sessao)):
    sala = sessao.get(Sala, sala_id)

    if not sala:
        # HTTPException é como devolvemos um erro "bonito" pro cliente
        # da API, com um código HTTP e uma mensagem clara.
        # 404 = "não encontrado".
        raise HTTPException(status_code=404, detail="Sala não encontrada.")

    return sala


# UPDATE - atualizar uma sala existente

# PUT (ou PATCH) é o verbo usado, por convenção, para ATUALIZAR algo
# que já existe. Aqui aceitamos atualização parcial: só os campos que
# vierem preenchidos no SalaUpdate serão alterados.

@app.put("/salas/{sala_id}", response_model=Sala)
def atualizar_sala(sala_id: int, dados: SalaUpdate, sessao: Session = Depends(obter_sessao)):
    sala = sessao.get(Sala, sala_id)

    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")

    # exclude_unset=True pega SÓ os campos que o cliente realmente
    # enviou no JSON, ignorando os que ficaram de fora (que continuam None).
    dados_para_atualizar = dados.model_dump(exclude_unset=True)

    for campo, valor in dados_para_atualizar.items():
        setattr(sala, campo, valor)

    sessao.add(sala)
    sessao.commit()
    sessao.refresh(sala)

    return sala


# DELETE - remover uma sala
@app.delete("/salas/{sala_id}")
def deletar_sala(sala_id: int, sessao: Session = Depends(obter_sessao)):
    sala = sessao.get(Sala, sala_id)

    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")

    sessao.delete(sala)
    sessao.commit()

    return {"mensagem": f"Sala {sala_id} deletada com sucesso."}

@app.get("users", response_model=List[User])
def listar_users( sessao: Session = Depends(obter_sessao)):
    users = sessao.exec(select(User)).all()
    return users