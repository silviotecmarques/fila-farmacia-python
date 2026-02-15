import json
import os

DATA_PATH = "data/balconistas.json"

def garantir_diretorio():
    # Cria a pasta data se ela não existir
    if not os.path.exists("data"):
        os.makedirs("data")

def salvar_dados(balconistas):
    garantir_diretorio()
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(balconistas, f, indent=4, ensure_ascii=False)

def carregar_dados():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []