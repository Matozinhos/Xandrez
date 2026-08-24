class Casa: # Classe de casa do tabuleiro, para guardar a posicao e representar nos botoes
    def __init__(self, linha :int, coluna :int, peca = None):
        self._linha = linha
        self._coluna = coluna
        self.peca = peca

    def __str__(self) -> tuple[int,int]:
        return (self._linha, self._coluna)
    
    def is_vazia(self) -> bool:
        return self.peca is None