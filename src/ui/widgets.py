# src/ui/widgets.py
import tkinter as tk
from tkinter import ttk

class FilaTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns=("Nome", "Funcao", "Atend", "Med", "Total"), show="headings")
        
        # Definição dos Cabeçalhos
        self.heading("Nome", text="NOME")
        self.heading("Funcao", text="FUNÇÃO")
        self.heading("Atend", text="ATEND.")
        self.heading("Med", text="TEMPO MEDIO")
        self.heading("Total", text="TOTAL")
        
        # Alinhamento e Largura
        self.column("Nome", width=200, anchor="w")
        self.column("Funcao", width=150, anchor="center")
        self.column("Atend", width=80, anchor="center")
        self.column("Med", width=120, anchor="center")
        self.column("Total", width=100, anchor="center")