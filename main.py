from classes.Tabuleiro import Tabuleiro
from interface import JanelaXadrez
t = Tabuleiro()

t.montar_posicao_inicial()

j = JanelaXadrez()

j.jogo.tabuleiro.montar_posicao_inicial()
j.atualizar_tabuleiro()
j.mainloop()    
