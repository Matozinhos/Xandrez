from Peca import Peca

class Tabuleiro:
    def __init__(self):
        self.matrizTabuleiro = [[ () for _ in range(8)] for _ in range(8)]
        self.pecas_em_jogo = []

    def dentro_dos_limite(self, linha, coluna) -> bool:
        pass

    def get_peca(self, linha, coluna) -> Peca:
        pass

    def get_casas_atacadas(self, linha, coluna) -> list[tuple[int,int]]:
        pass