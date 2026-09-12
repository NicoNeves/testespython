
"""
Script auxiliar TEMPORÁRIO. Apaga o arquivo do banco e
recria as tabelas do zero, já com o formato mais atual dos models.
 
Use isso sempre que mudar algo em models.py
 
FUTURAMENTE será EXCLUÍDO e substituido por uma ferramenta de migração de banco de dados (Alembic).
 
Como rodar:
    python reset_db.py
"""

import os
from app.database import DATABASE_URL, criar_banco_e_tabelas

# DATABASE_URL é "sqlite:///salas.db", então tiramos o prefixo "sqlite:///" pra ficar só com o nome do arquivo.
CAMINHO_DO_ARQUIVO = DATABASE_URL.replace("sqlite:///","")

def resetar_banco():
    if os.path.exists(CAMINHO_DO_ARQUIVO):
        os.remove(CAMINHO_DO_ARQUIVO)
        print(f"Arquivo {CAMINHO_DO_ARQUIVO} apagado.")
    else:
        print(f"Arquivo {CAMINHO_DO_ARQUIVO} não existia, então nada foi apagado")

    criar_banco_e_tabelas()
    print("Banco recriado com formato atual dos models.")

if __name__ == "__main__":
    #Essa confirmação existe só pra ngm acabar apagando algo sem querer.
    resposta = input(f"Tem certeza que quer resetar o banco de dados {CAMINHO_DO_ARQUIVO}? (s/n) ")
    if resposta.lower() == "s":
        resetar_banco()
    else:
        print("Operação cancelada. Nada foi apagado.")