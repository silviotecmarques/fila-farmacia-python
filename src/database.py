# src/database.py
import json, os

class Database:
    def __init__(self, filename="database.json"):
        self.path = filename
        self.dados = self.carregar_dados()

    def carregar_dados(self):
        if not os.path.exists(self.path):
            return {"profissionais": [], "fila": []}
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "profissionais" not in data: data["profissionais"] = []
                if "fila" not in data: data["fila"] = []
                return data
        except:
            return {"profissionais": [], "fila": []}

    def salvar_dados(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)