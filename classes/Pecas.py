class Peca: # SuperClass
    def __init__(self, cor : str, linha : str, coluna : str):
        self.cor = cor
        self._linha = linha
        self._coluna = coluna

    def __str__(self):
        return f"{type(self).__name__} ({self.cor}) em {self.posicao()}"

    def mover_para(self, linha, coluna) :
        self._linha, self._coluna = linha, coluna

    def posicao_def(self, linha :int, coluna:int):
        self._linha, self._coluna = linha, coluna
        
    def posicao(self) :
        return (self._linha, self._coluna)
    
    def movimentos_validos(self, tabuleiro) -> list[tuple[int,int]] :
        # Retornara uma lista com os movimentos possiveis para a peca, so faz sentido para as subclasses
        return None

    def movimento_em_linhas(self, tabuleiro, direcoes) -> list[tuple[int,int]]:
        # Logica para implementar na torre, bispo e rainha

        movimentos = []

        for delta_linha, delta_coluna in direcoes:
            linha, coluna = self._linha + delta_linha, self._coluna + delta_coluna

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

    def movimentos_validos(self, tabuleiro )  -> list[tuple[int,int]] :
        movimentos = []
        direcao = -1 if self.cor == "branco" else 1
        linha_inicial = 6 if self.cor == "branco" else 1

        frente = (self._linha + direcao, self._coluna)
        if tabuleiro.dentro_do_limite(*frente) and tabuleiro.get_peca(*frente) is None:
            movimentos.append(frente)

            if self._linha == linha_inicial:
                dois_frente = (self._linha + 2 * direcao, self._coluna)
                if tabuleiro.get_peca(*dois_frente) is None:
                    movimentos.append(dois_frente)

        for delta_coluna in (-1,1):
            diagonal = (self._linha + direcao, self._coluna + delta_coluna)
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
            linha, coluna = self._linha + delta_linha, self._coluna + delta_coluna

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

    def movimentos_validos(self, tabuleiro) -> list[tuple[int,int]]:

        movimentos_impossiveis = []
        for delta_linha, delta_coluna in self.__direcoes:
            linha, coluna = self._linha, self._coluna
            
        while tabuleiro.dentro_dos_limite(linha, coluna):
            linha += delta_linha
            coluna += delta_coluna

            peca_alvo = tabuleiro.get_peca(linha, coluna)
            
            if peca_alvo is None:
                break
            if peca_alvo.cor == self.cor:
                break

            if (delta_linha, delta_coluna) in [(-1, 0), (1, 0), (0, -1), (0, 1)] :
                if isinstance(peca_alvo, (Torre, Rainha)):
                    movimentos_impossiveis.append((linha, coluna))
            else:
                if isinstance(peca_alvo, (Bispo, Rainha)):
                    movimentos_impossiveis.append((linha,coluna))

        movimentos = []
        casas_atacadas = tabuleiro.get_casas_atacadas() 
        for delta_linha, delta_coluna in self.__direcoes:
            atacada = False 
            linha, coluna = self._linha + delta_linha, self._coluna + delta_coluna

            if not tabuleiro.dentro_dos_limite(linha, coluna) or (linha,coluna) in movimentos_impossiveis:
                continue

            if (linha, coluna) in casas_atacadas:
                continue

            peca_alvo = tabuleiro.get_peca(linha, coluna)
            if peca_alvo is None or peca_alvo.cor != self.cor:
                movimentos.append((linha, coluna))

        return movimentos