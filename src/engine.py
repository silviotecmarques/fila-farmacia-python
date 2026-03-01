# src/engine.py

class FilaEngine:
    def __init__(self, database):
        self.db = database
        self.cadastro = self.db.dados["profissionais"]
        
        # Reset da fila na inicialização para começar o dia limpo
        self.db.dados["fila"] = []
        self.fila = self.db.dados["fila"]
        self.db.salvar_dados()

    def cadastrar_novo(self, nome, foto):
        # LÓGICA BLINDADA: Encontra o maior ID atual e soma 1
        # Se não houver ninguém, o ID inicial será 1
        max_id = 0
        if self.cadastro:
            max_id = max(p['id'] for p in self.cadastro)
            
        novo = {"id": max_id + 1, "nome": nome, "foto": foto}
        self.cadastro.append(novo)
        self.db.salvar_dados()

    def deletar_membro(self, b_id):
        # Remove do cadastro e da fila de hoje
        self.db.dados["profissionais"] = [p for p in self.db.dados["profissionais"] if p['id'] != b_id]
        self.cadastro = self.db.dados["profissionais"]
        self.db.dados["fila"] = [f for f in self.db.dados["fila"] if f['id'] != b_id]
        self.fila = self.db.dados["fila"]
        self.db.salvar_dados()

    def alternar_na_fila(self, b_id):
        membro = next((p for p in self.cadastro if p['id'] == b_id), None)
        if not membro: return
        
        pos = next((i for i, f in enumerate(self.fila) if f['id'] == b_id), None)
        if pos is not None:
            self.fila.pop(pos)
        else:
            self.fila.append(membro)
        self.db.salvar_dados()

    def proximo(self):
        if len(self.fila) > 1:
            p = self.fila.pop(0)
            self.fila.append(p)
            self.db.salvar_dados()