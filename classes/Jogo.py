from classes.Tabuleiro import Tabuleiro
from classes.Pecas import *
from classes.Jogador import Jogador

class Jogo:
    def __init__(self, jogador_branca : str = "brancas", jogador_preta : str = "pretas" ):
        self.tabuleiro = Tabuleiro()
        self.jogadores = [
            Jogador(jogador_branca, "branco"),
            Jogador(jogador_preta, "preto")
        ]
        self.turno_atual = "branco"
        self.historico_de_jogadas : list[tuple[Peca, int,int, bool]] = []

    def jogador_da_vez(self) -> Jogador:
        return next(j for j in self.jogadores if j.cor == self.turno_atual)

    def trocar_turno(self):
        self.turno_atual = "preto" if self.turno_atual == "branco" else "branco"

    def mover_peca(self, linha_origem, coluna_origem, linha_destino, coluna_destino) -> bool:
        peca = self.tabuleiro.get_peca(linha_origem, coluna_origem)

        if peca is None or peca.cor != self.turno_atual:
            return False

        peca_capturar = self.tabuleiro.mover_peca(linha_origem, coluna_origem, linha_destino, coluna_destino)

        if peca_capturar == False:
            return False

        if peca_capturar is not None:
            self.jogador_da_vez().registrar_captura(peca_capturar)
            self.historico_de_jogadas.append((peca, linha_destino, coluna_destino, True))
            self.trocar_turno()
            return True
        self.historico_de_jogadas.append((peca, linha_destino, coluna_destino, False))
        self.trocar_turno()
        return True 