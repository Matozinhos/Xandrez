from Peca import Peca

class Casa: # Classe de casa do tabuleiro, para guardar a posicao e representar nos botoes
    def __init__(self, linha :int, coluna :int, peca : Peca = None):
        self.__linha = linha
        self.__coluna = coluna
        self.peca = peca

    def __str__(self) -> tuple[int,int]:
        return (self.__linha, self.__coluna)
    
    def is_vazia(self) -> bool:
        return self.peca is None