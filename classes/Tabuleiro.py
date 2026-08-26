from classes.Pecas import *
from classes.Casa import Casa

class Tabuleiro:
    def __init__(self):
        self.TAMANHO = 8
        self.matrizTabuleiro = [[Casa(linha, coluna) for coluna in range(self.TAMANHO)] for linha in range(self.TAMANHO)]
        self.pecas_em_jogo = []

    def dentro_dos_limite(self, linha :int, coluna :int) -> bool:
        return 0 <= linha < self.TAMANHO and 0 <= coluna < self.TAMANHO

    def get_peca(self, linha:int, coluna:int) -> Peca:
        return self.matrizTabuleiro[linha][coluna].peca

    def get_casa(self, linha:int, coluna:int) -> Casa:
        return self.matrizTabuleiro[linha][coluna]

    def remover_peca(self, linha:int, coluna:int) :
        print("Removeu peca")
        self.matrizTabuleiro[linha][coluna].peca = None

    def colocar_peca(self, peca : Peca, linha:int, coluna:int):
        print("Colocou Peca")
        peca.posicao_def(linha, coluna)
        self.matrizTabuleiro[linha][coluna].peca = peca

    def get_casas_atacadas(self, linha :int, coluna :int) -> list[tuple[int,int]]:
        casas_atacadas = []
        for linha in range(self.TAMANHO):
            for coluna in range(self.TAMANHO):
                casa = self.matrizTabuleiro[linha][coluna]
                if not casa.is_vazia() or not isinstance(self.get_peca(linha, coluna), Rei):
                    peca = casa.peca
                    casas_atacadas.append(peca.movimentos_validos(self))
        return casas_atacadas

    def mover_peca(self, linha0, coluna0, linhaF, colunaF) -> bool:
        peca = self.get_peca(linha0, coluna0)
        print("Mover Peca")
        
        if peca is None:
            print(self)
            raise ValueError("Não há peca na casa de origem")

        movimentos = peca.movimentos_validos(self)
        if (linhaF, colunaF) in movimentos:
            peca_capturar = None
            if not self.get_peca(linhaF, colunaF) is None:
                peca_capturar = self.get_peca(linhaF, colunaF)

            self.remover_peca(linha0, coluna0)
            self.colocar_peca(peca, linhaF, colunaF)
            return peca_capturar
        else:
            return False

    def montar_posicao_inicial(self):
        ordem = [Torre, Cavalo, Bispo, Rainha, Rei, Bispo, Cavalo, Torre]

        for coluna, ClassPeca in enumerate(ordem):
            self.colocar_peca(ClassPeca("preto", 0, coluna), 0, coluna)
            self.colocar_peca(ClassPeca("branco", 7, coluna), 7, coluna)
 
        for coluna in range(self.TAMANHO):
            self.colocar_peca(Peao("preto", 1, coluna), 1, coluna)
            self.colocar_peca(Peao("branco", 6, coluna), 6, coluna)

    def __str__(self):
        simbolos = {
            "Peao": "P", "Torre": "T", "Cavalo": "C",
            "Bispo": "B", "Rainha": "Q", "Rei": "K",
        }
        linhas_texto = []
        for linha in self.matrizTabuleiro:
            texto = []
            for casa in linha:
                if casa.is_vazia():
                    texto.append(".")
                else:
                    simbolo = simbolos[type(casa.peca).__name__]
                    texto.append(simbolo.upper() if casa.peca.cor == "branco" else simbolo.lower())
            linhas_texto.append(" ".join(texto))
        return "\n".join(linhas_texto)