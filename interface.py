import customtkinter as ctk
import os
from PIL import Image
from classes.Jogo import Jogo

lista_pecas_para_imagens = [
    ('branco', 'Peao'), ('branco', 'Torre'), ('branco', 'Cavalo'),
    ('branco', 'Bispo'), ('branco', 'Rainha'), ('branco', 'Rei'),
    ('preto', 'Peao'), ('preto', 'Torre'), ('preto', 'Cavalo'),
    ('preto', 'Bispo'), ('preto', 'Rainha'), ('preto', 'Rei')
]

SIMBOLOS =  {}

for cor, peca in lista_pecas_para_imagens:
    diretorio_atual = os.path.dirname(__file__)
    caminho_imagem = os.path.join(diretorio_atual, "imgs", f"Chess_{peca.lower()}_{cor}_Sprite.png")

    imagem = Image.open(caminho_imagem)
    SIMBOLOS[(cor,peca)] = imagem


imagem_vazia = Image.open(os.path.join(diretorio_atual,"imgs", "pngg.png"))

COR_CASA_CLARA = "#EEEED2"
COR_CASA_ESCURA = "#769656"
COR_SELECIONADA = "#F6F669"
COR_MOVIMENTO_VALIDO = "#DA7D7A"
 
 
class JanelaXadrez(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Xadrez")
        self.geometry("640x700")
        self.resizable(False, False)

        self.jogo = Jogo("Jogador1", "Jogador2")
        self.casa_selecionada : tuple[int,int] = None      
        self.movimentos_destacados : list[tuple[int,int]] = []   
        self.botoes = {}  

        self.label_turnos()
        self.montar_tabuleiro()
        self.atualizar_tabuleiro()

    def selecionar_casa(self, linha, coluna):
        peca = self.jogo.tabuleiro.get_peca(linha, coluna)
        self.casa_selecionada = (linha,coluna)
        self.movimentos_destacados = peca.movimentos_validos(self.jogo.tabuleiro)
        

    def limpar_selecao(self):
        self.casa_selecionada = None
        self.movimentos_destacados = []

    def label_turnos(self):
        self.label_turnos = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_turnos.pack(pady=(15,5))

    def montar_tabuleiro(self):
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
                    hover_color= cor_fundo,
                    command=lambda l = linha, c = coluna: self.clicar_casa(l,c)
                )
                botao.grid(row = linha, column= coluna)
                self.botoes[(linha, coluna)] = botao

    def clicar_casa(self, linha, coluna):
        if self.casa_selecionada is not None:
            linha_origem, coluna_origem = self.casa_selecionada

            if (linha,coluna) in self.movimentos_destacados:
                self.jogo.mover_peca(linha_origem, coluna_origem, linha, coluna)
                self.limpar_selecao()
                self.atualizar_tabuleiro()
                return

            self.limpar_selecao()

            peca = self.jogo.tabuleiro.get_peca(linha,coluna)
            if peca is not None and peca.cor == self.jogo.turno_atual:
                self.selecionar_casa(linha, coluna)

            self.atualizar_tabuleiro()
            return
        peca = self.jogo.tabuleiro.get_peca(linha,coluna)
        if peca is not None and peca.cor == self.jogo.turno_atual:
            self.selecionar_casa(linha,coluna)
            self.atualizar_tabuleiro()

    def atualizar_casa(self,linha,coluna):
        botao = self.botoes[(linha,coluna)]
        peca = self.jogo.tabuleiro.get_peca(linha,coluna)

        if peca:
            imagem = SIMBOLOS[(peca.cor, type(peca).__name__)]
            imagem_peca = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=(68,68)
            )
            botao.configure(image=imagem_peca)
        else:
            imagem_peca = ctk.CTkImage(
                light_image=imagem_vazia,
                dark_image=imagem_vazia,
                size=(68,68)
            )
            botao.configure(image=imagem_peca)
            
        cor_base = COR_CASA_CLARA if (linha + coluna) % 2 == 0 else COR_CASA_ESCURA

        if (linha,coluna) == self.casa_selecionada:
            cor = COR_SELECIONADA
        elif (linha, coluna) in self.movimentos_destacados:
            cor = COR_MOVIMENTO_VALIDO
        else:
            cor = cor_base

        botao.configure(fg_color= cor, hover_color = cor)

    def atualizar_tabuleiro(self):
        for linha in range(8):
            for coluna in range(8):
                self.atualizar_casa(linha, coluna)

        print("atualizou o tabuleiro")
        nome_jogador = self.jogo.jogador_da_vez().nome
        self.label_turnos.configure(
            text = f"Vez de: {nome_jogador} ({self.jogo.turno_atual}) Casa Selecionada = {self.casa_selecionada}"
        )

