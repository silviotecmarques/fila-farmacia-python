from src.core.storage import salvar_dados, carregar_dados

class GerenciadorFila:
    def __init__(self):
        self.balconistas = carregar_dados()

    def adicionar(self, nome, avatar_path):
        novo_id = max([b["id"] for b in self.balconistas], default=0) + 1
        novo = {
            "id": novo_id,
            "nome": nome,
            "avatar": avatar_path,
            "atendimentos": 0
        }
        self.balconistas.append(novo)
        salvar_dados(self.balconistas)

    def proximo(self):
        if len(self.balconistas) > 0:
            atendente = self.balconistas.pop(0)
            atendente["atendimentos"] += 1
            self.balconistas.append(atendente)
            salvar_dados(self.balconistas)
            return atendente
        return None

    def pular(self):
        if len(self.balconistas) > 1:
            atendente = self.balconistas.pop(0)
            self.balconistas.append(atendente)
            salvar_dados(self.balconistas)

    def remover(self, id_balconista):
        self.balconistas = [b for b in self.balconistas if b["id"] != id_balconista]
        salvar_dados(self.balconistas)