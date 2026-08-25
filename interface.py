import customtkinter as ctk
from classes.Jogo import Jogo


COR_CASA_CLARA = "#EEEED2"
COR_CASA_ESCURA = "#769656"
COR_SELECIONADA = "#F6F669"
COR_MOVIMENTO_VALIDO = "#BACA44"
 
 
class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()
 
