from Tabuleiro import Tabuleiro as tabuleiro

class Peca: # SuperClass
    def __init__(self, cor : str, linha : str, coluna : str):
        self.cor = cor
        self.__linha = linha
        self.__coluna = coluna

    def __str__(self):
        return f"{type(self).__name__} ({self.cor}) em {self.posicao()}"

    def mover_para(self, linha, coluna) :
        self.__linha, self.__coluna = linha, coluna

    def posicao(self) :
        return (self.__linha, self.__coluna)
    
    def movimentos_validos(self, tabuleiro : tabuleiro) -> list[tuple[int,int]] :
        # Retornara uma lista com os movimentos possiveis para a peca, so faz sentido para as subclasses
        return None

    def movimento_em_linhas(self, tabuleiro : tabuleiro, direcoes) -> list[tuple[int,int]]:
        # Logica para implementar na torre, bispo e rainha

        movimentos = []

        for delta_linha, delta_coluna in direcoes:
            linha, coluna = self.__linha + delta_linha, self.__coluna + delta_coluna

            while tabuleiro.dentro_dos_limite(linha, coluna):
                peca_alvo = tabuleiro.get_peca(linha, coluna)

                if peca_alvo is None:
                    movimentos.append((linha,coluna))
                else:
                    if peca_alvo.cor != self.cor:
                        movimentos.append((linha,coluna))
                    break

                linha += delta_linha
                coluna += delta_coluna

        return movimentos

# Subclasses

class Peao(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)

    def movimentos_validos(self, tabuleiro : tabuleiro)  -> list[tuple[int,int]] :
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

class Torre(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)
        self.__direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def movimentos_validos(self, tabuleiro) -> list[tuple[int,int]]:
        return self.movimento_em_linhas(tabuleiro, self.__direcoes)

class Bispo(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)
        self.__direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def movimentos_validos(self, tabuleiro):
        return self.movimento_em_linhas(tabuleiro, self.__direcoes)

class Rainha(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)
        self.__direcoes = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

    def movimentos_validos(self, tabuleiro):
        return self.movimento_em_linhas(tabuleiro, self.__direcoes)

class Cavalo(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)
        self.__saltos = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]

    def movimentos_validos(self, tabuleiro):
        movimentos =[]
        for delta_linha, delta_coluna in self.__saltos:
            linha, coluna = self.__linha + delta_linha, self.__coluna + delta_coluna

            if not tabuleiro.dentro_dos_limite(linha, coluna):
                continue

            peca_alvo = tabuleiro.get_peca(linha, coluna)
            if peca_alvo is None or peca_alvo.cor != self.cor:
                movimentos.append((linha,coluna))
        return movimentos

class Rei(Peca):
    def __init__(self, cor, linha, coluna):
        super().__init__(cor, linha, coluna)
        self.check = False
        self.__direcoes = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1),
        ]

    def movimentos_validos(self, tabuleiro):

        movimentos_impossiveis = []
        for delta_linha, delta_coluna in self.__direcoes:
            linha, coluna = self.__linha, self.__coluna
            
        while tabuleiro.dentro_dos_limite(linha, coluna):
            linha += delta_linha
            coluna += delta_coluna

            peca_alvo = tabuleiro.get_peca(linha, coluna)
            
            if peca_alvo is None:
                break
            if peca_alvo.cor == self.cor:
                break

            if (delta_linha, delta_coluna) in [(-1, 0), (1, 0), (0, -1), (0, 1)] # se tiver aqui e é uma torre ou rainha == tmnc
                if isinstance(peca_alvo, (Torre, Rainha)):
                    movimentos_impossiveis.append((linha, coluna))
            else:
                if isinstance(peca_alvo, (Bispo, Rainha)):
                    movimentos_impossiveis.append((linha,coluna))

        movimentos = []

        for delta_linha, delta_coluna in self.__direcoes:
            atacada = False 
            linha, coluna = self.__linha + delta_linha, self.__coluna + delta_coluna

            if not tabuleiro.dentro_dos_limite(linha, coluna) or (linha,coluna) in movimentos_impossiveis:
                continue

            for delta_l, delta_c in tabuleiro.get_casas_atacadas() :
                if (linha, coluna) == (delta_l, delta_c):
                    continue

            peca_alvo = tabuleiro.get_peca(linha, coluna)
            if peca_alvo is None or peca_alvo.cor != self.cor:
                movimentos.append((linha, coluna))

        return movimentos