class Jogador:
    def __init__(self, nome : str, cor : str):
        if cor not in ("branco", "preto"):
            raise ValueError("Cor Invalida, Branco ou Preto")

        self.nome = nome
        self.cor = cor
        self.pecas_capturadas = []

    def registrar_captura(self, peca):
        self.pecas_capturadas.append(peca)

    def __str__(self):
        return f"{self.nome} ({self.cor})"