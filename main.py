from classes.Tabuleiro import Tabuleiro
from interface import JanelaXadrez
t = Tabuleiro()

t.montar_posicao_inicial()

j = JanelaXadrez()
j.mainloop()

print(t)