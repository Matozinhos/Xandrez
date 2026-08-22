import Tabuleiro

class Peca: # SuperClass
    def __init__(self, cor : str, linha : str, coluna : str):
        self.cor = cor
        self.__linha = linha
        self.__coluna = coluna

    def __str__(self):
        return f"{type(self).__name__} ({self.cor}) em {self.posicao()}"

    def movimentos_validos(self, tabuleiro) -> list[tuple[int,int]] :
        # Retornara uma lista com os movimentos possiveis para a peca, so faz sentido para as subclasses
        pass    

    def mover_para(self, linha, coluna) :
        self.__linha, self.__coluna = linha, coluna

    def posicao(self) :
        return (self.__linha, self.__coluna)

class Peao(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)

    def movimentos_validos(self, tabuleiro)  -> list[tuple[int,int]] :
        movimentos = []
        direcao = -1 if self.cor == "branco" else 1
        linha_inicial = 6 if self.cor == "branco" else 1

        frente = (self.__linha + direcao, self.__coluna)
        if tabuleiro.dentro_do_limite(*frente) and tabuleiro.get_peca(*frente) is None:
            movimentos.append(frente)

            if self.__linha == linha_inicial:
                dois_frente = (self.__linha + 2 * direcao, self.__coluna)
                if tabuleiro.get_peca(*dois_frente) is None:
                    movimentos.append(dois_frente)

        for delta_coluna in (-1,1):
            diagonal = (self.__linha + direcao, self.__coluna + delta_coluna)
            if tabuleiro.dentro_do_limite(*diagonal):
                peca_alvo = tabuleiro.get_peca(*diagonal)
                if peca_alvo is not None and peca_alvo.cor != self.cor:
                    movimentos.append(diagonal)
        return movimentos