import customtkinter as ctk
from classes.Jogo import Jogo

SIMBOLOS = {
    ("branco", "Peao"): "♙", ("branco", "Torre"): "♖", ("branco", "Cavalo"): "♘",
    ("branco", "Bispo"): "♗", ("branco", "Rainha"): "♕", ("branco", "Rei"): "♔",
    ("preto", "Peao"): "♟", ("preto", "Torre"): "♜", ("preto", "Cavalo"): "♞",
    ("preto", "Bispo"): "♝", ("preto", "Rainha"): "♛", ("preto", "Rei"): "♚",
}


COR_CASA_CLARA = "#EEEED2"
COR_CASA_ESCURA = "#769656"
COR_SELECIONADA = "#F6F669"
COR_MOVIMENTO_VALIDO = "#BACA44"
 
 
class JanelaXadrez(ctk.CTk):
    def __init__(self):
        super().__init__()
 
        self.title("Xadrez")
        self.geometry("640x700")
        self.resizable(False, False)
 
        self.jogo = Jogo("Jogador 1", "Jogador 2")
        self.casa_selecionada = None      # (linha, coluna) da peça selecionada, ou None
        self.movimentos_destacados = []   # lista de (linha, coluna) que a peça pode alcançar
        self.botoes = {}                  # mapa (linha, coluna) -> CTkButton
 
        self._montar_label_turno()
        self._montar_tabuleiro()
        self._atualizar_tabuleiro()
 
    def _montar_label_turno(self):
        self.label_turno = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_turno.pack(pady=(15, 5))
 
    def _montar_tabuleiro(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=10)
 
        for linha in range(8):
            for coluna in range(8):
                cor_fundo = COR_CASA_CLARA if (linha + coluna) % 2 == 0 else COR_CASA_ESCURA
 
                botao = ctk.CTkButton(
                    frame,
                    text="",
                    width=70,
                    height=70,
                    corner_radius=0,
                    fg_color=cor_fundo,
                    hover_color=cor_fundo,
                    font=ctk.CTkFont(size=32),
                    text_color="black",
                    command=lambda l=linha, c=coluna: self._clicar_casa(l, c),
                )
                botao.grid(row=linha, column=coluna)
                self.botoes[(linha, coluna)] = botao
 
    def _clicar_casa(self, linha, coluna):
        # Caso 1: já tem uma peça selecionada -> essa clique é o destino
        if self.casa_selecionada is not None:
            origem = self.casa_selecionada
 
            if (linha, coluna) in self.movimentos_destacados:
                self.jogo.mover_peca(*origem, linha, coluna)
                self._limpar_selecao()
                self._atualizar_tabuleiro()
                return
 
            # Clicou em outra casa (não era um movimento válido): reseta seleção
            self._limpar_selecao()
 
            # Se clicou em outra peça própria, já seleciona ela em seguida
            peca = self.jogo.tabuleiro.get_peca(linha, coluna)
            if peca is not None and peca.cor == self.jogo.turno_atual:
                self._selecionar_casa(linha, coluna)
 
            self._atualizar_tabuleiro()
            return
 
        # Caso 2: nenhuma peça selecionada ainda -> essa clique escolhe a peça
        peca = self.jogo.tabuleiro.get_peca(linha, coluna)
        if peca is not None and peca.cor == self.jogo.turno_atual:
            self._selecionar_casa(linha, coluna)
            self._atualizar_tabuleiro()
 
    def _selecionar_casa(self, linha, coluna):
        peca = self.jogo.tabuleiro.get_peca(linha, coluna)
        self.casa_selecionada = (linha, coluna)
        self.movimentos_destacados = peca.movimentos_validos(self.jogo.tabuleiro)
 
    def _limpar_selecao(self):
        self.casa_selecionada = None
        self.movimentos_destacados = []
 
    def _atualizar_tabuleiro(self):
        for linha in range(8):
            for coluna in range(8):
                self._atualizar_casa(linha, coluna)
 
        nome_jogador = self.jogo.jogador_da_vez().nome
        self.label_turno.configure(
            text=f"Vez de: {nome_jogador} ({self.jogo.turno_atual})"
        )
 
    def _atualizar_casa(self, linha, coluna):
        botao = self.botoes[(linha, coluna)]
        peca = self.jogo.tabuleiro.get_peca(linha, coluna)
 
        simbolo = SIMBOLOS[(peca.cor, type(peca).__name__)] if peca else ""
        botao.configure(text=simbolo)
 
        cor_base = COR_CASA_CLARA if (linha + coluna) % 2 == 0 else COR_CASA_ESCURA
 
        if (linha, coluna) == self.casa_selecionada:
            cor = COR_SELECIONADA
        elif (linha, coluna) in self.movimentos_destacados:
            cor = COR_MOVIMENTO_VALIDO
        else:
            cor = cor_base
 
        botao.configure(fg_color=cor, hover_color=cor)
 
 
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = JanelaXadrez()
    app.mainloop()