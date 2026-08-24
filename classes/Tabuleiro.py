from Peca import *
from Casa import Casa

class Tabuleiro:
    def __init__(self):
        self.TAMANHO = 8
        self.matrizTabuleiro = [[Casa(linha, coluna) for coluna in range(self.TAMANHO)] for linha in range(self.TAMANHO)]
        self.pecas_em_jogo = []

    def dentro_dos_limite(self, linha :int, coluna :int) -> bool:
        return 0 <= linha < self.TAMANHO and 0 <= coluna < self.TAMANHO

    def get_peca(self, linha:int, coluna:int) -> Peca:
        return self.matrizTabuleiro[linha][coluna]

    def get_casas_atacadas(self, linha :int, coluna :int) -> list[tuple[int,int]]:
        casas_atacadas = []
        for linha in range(self.TAMANHO):
            for coluna in range(self.TAMANHO):
                casa = self.matrizTabuleiro[linha][coluna]
                if not casa.is_vazia():
                    peca = casa.peca
                    casas_atacadas.append(peca.movimentos_validos(self))
        return casas_atacadas