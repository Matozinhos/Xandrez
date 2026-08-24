from classes.Tabuleiro import Tabuleiro

t = Tabuleiro()

t.montar_posicao_inicial()


t.mover_peca(0,0, 4,4)
t.mover_peca(0,1, 2,2)
t.mover_peca(2,2, 3, 0)
print(t)