# src/engine.py

class FilaEngine:
    def __init__(self, db):
        self.db = db
        self.cadastro = self.db.load("balconistas.json", default=[])
        self.fila = []

    def cadastrar_novo(self, nome, funcao, foto):
        novo = {"id": len(self.cadastro) + 1, "nome": nome, "funcao": funcao, "foto": foto}
        self.cadastro.append(novo)
        self.db.save("balconistas.json", self.cadastro)
        return novo

    def alternar_na_fila(self, balconista_id):
        """Adiciona se não estiver, remove se já estiver."""
        # Verifica se já está na fila
        for i, item in enumerate(self.fila):
            if item['id'] == balconista_id:
                self.fila.pop(i) # Remove
                return "removido"
        
        # Se não encontrou, adiciona
        for b in self.cadastro:
            if b['id'] == balconista_id:
                item = b.copy()
                item.update({"atendimentos": 0, "tempo_total": 0, "tempo_atual": 0, "tempo_medio": "00:00"})
                self.fila.append(item)
                return "adicionado"
        return None

    def atender(self):
        if not self.fila: return
        b = self.fila.pop(0)
        b["atendimentos"] += 1
        b["tempo_total"] += b["tempo_atual"]
        b["tempo_atual"] = 0
        if b["atendimentos"] > 0:
            media = b["tempo_total"] // b["atendimentos"]
            m, s = divmod(media, 60)
            b["tempo_medio"] = f"{m:02d}:{s:02d}"
        self.fila.append(b)

    def pular(self):
        if not self.fila: return
        b = self.fila.pop(0)
        b["tempo_atual"] = 0
        self.fila.append(b)

    def tick(self):
        if self.fila: self.fila[0]["tempo_atual"] += 1