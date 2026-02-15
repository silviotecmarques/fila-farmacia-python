from .storage import salvar_dados, carregar_dados

class GerenciadorFila:
    def __init__(self):
        self.balconistas = carregar_dados()

    def adicionar(self, nome, avatar_path):
        novo = {
            "id": len(self.balconistas) + 1,
            "nome": nome,
            "avatar": avatar_path,
            "atendimentos": 0
        }
        self.balconistas.append(novo)
        salvar_dados(self.balconistas)

    def proximo(self):
        if len(self.balconistas) > 1:
            # Pega o primeiro, incrementa atendimento e move para o fim
            atendente = self.balconistas.pop(0)
            atendente["atendimentos"] += 1
            self.balconistas.append(atendente)
            salvar_dados(self.balconistas)
            return atendente
        return self.balconistas[0] if self.balconistas else None

    def remover(self, id_balconista):
        self.balconistas = [b for b in self.balconistas if b["id"] != id_balconista]
        salvar_dados(self.balconistas)