#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print Dialog Simulator
Recria a interface de impressão mostrada na imagem
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

class PrintDialog:
    def __init__(self, root):
        self.root = root
        self.root.title("Imprimir Imagens")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Variáveis de controle
        self.printer_var = tk.StringVar()
        self.paper_size_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.paper_type_var = tk.StringVar()
        self.copies_var = tk.StringVar()
        
        # Valores padrão
        self.printer_var.set("MONTY-SCTI - HP LaserJet MFI")
        self.paper_size_var.set("A4")
        self.quality_var.set("Normal")
        self.paper_type_var.set("Padrão da impressora")
        self.copies_var.set("4")
        
        self.image_files = []
        self.current_preview = 0
        
        # Configurar UI
        self.setup_ui()
        
    def setup_ui(self):
        """Configura toda a interface"""
        
        # Frame superior azul com título
        header = tk.Frame(self.root, bg="#0066CC", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Imprimir Imagens", 
                        font=("Arial", 12, "bold"), 
                        fg="white", bg="#0066CC")
        title.pack(side=tk.LEFT, padx=15, pady=10)
        
        close_btn = tk.Button(header, text="✕", font=("Arial", 14), 
                              bg="#CC0000", fg="white", relief=tk.FLAT,
                              command=self.root.quit, width=2)
        close_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Seção de pergunta
        question_label = tk.Label(main_frame, text="Como deseja imprimir as imagens?",
                                 font=("Arial", 10), bg="white")
        question_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Frame de opções
        self.create_options_section(main_frame)
        
        # Separador
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=10)
        
        # Frame com preview e opções adicionais
        content_frame = tk.Frame(main_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Coluna esquerda - Preview
        self.create_preview_section(content_frame)
        
        # Coluna direita - Opções adicionais
        self.create_additional_options(content_frame)
        
        # Frame inferior com controles
        bottom_frame = tk.Frame(main_frame, bg="white")
        bottom_frame.pack(fill=tk.X, pady=10)
        
        self.create_bottom_controls(bottom_frame)
        
        # Frame de botões
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.create_buttons(button_frame)
    
    def create_options_section(self, parent):
        """Cria a seção de opções de impressão"""
        options_frame = tk.Frame(parent, bg="white")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Grid de opções
        options = [
            ("Impressora:", "printer", ["MONTY-SCTI - HP LaserJet MFI", 
                                        "Printer 2", "Printer 3"]),
            ("Tamanho do papel:", "paper_size", ["A3", "A4", "A5", "Ofício", "Carta"]),
            ("Qualidade:", "quality", ["Rascunho", "Normal", "Alta", "Máxima"]),
            ("Tipo de papel:", "paper_type", ["Padrão da impressora", 
                                             "Comum", "Fotográfico", "Espesso"])
        ]
        
        for i, (label, var_name, values) in enumerate(options):
            # Label
            lbl = tk.Label(options_frame, text=label, bg="white", width=20, anchor=tk.W)
            lbl.grid(row=0, column=i*2, sticky=tk.W, padx=5)
            
            # Combobox
            if var_name == "printer":
                combo = ttk.Combobox(options_frame, textvariable=self.printer_var, 
                                    values=values, state="readonly", width=20)
            elif var_name == "paper_size":
                combo = ttk.Combobox(options_frame, textvariable=self.paper_size_var,
                                    values=values, state="readonly", width=20)
            elif var_name == "quality":
                combo = ttk.Combobox(options_frame, textvariable=self.quality_var,
                                    values=values, state="readonly", width=20)
            else:  # paper_type
                combo = ttk.Combobox(options_frame, textvariable=self.paper_type_var,
                                    values=values, state="readonly", width=20)
            
            combo.grid(row=0, column=i*2+1, padx=5, sticky=tk.EW)
        
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)
        options_frame.columnconfigure(5, weight=1)
        options_frame.columnconfigure(7, weight=1)
    
    def create_preview_section(self, parent):
        """Cria a seção de preview das imagens"""
        preview_frame = tk.Frame(parent, bg="white")
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Preview área
        self.preview_canvas = tk.Canvas(preview_frame, bg="white", width=500, 
                                        height=300, relief=tk.SUNKEN)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Adicionar imagem de exemplo
        self.add_sample_preview()
        
        # Navegação de preview
        nav_frame = tk.Frame(preview_frame, bg="white")
        nav_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(nav_frame, text="1 de 1 página", bg="white").pack(side=tk.LEFT)
        
        tk.Button(nav_frame, text="◀", width=2).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="▶", width=2).pack(side=tk.LEFT)
    
    def add_sample_preview(self):
        """Adiciona um preview de exemplo na canvas"""
        # Desenhar um padrão de exemplo
        self.preview_canvas.create_rectangle(10, 10, 490, 290, fill="#E0E0E0", 
                                           outline="#999999", width=2)
        
        # Adicionar texto informativo
        self.preview_canvas.create_text(250, 150, 
                                       text="Preview das imagens\n(Selecione imagens para visualizar)",
                                       font=("Arial", 12), fill="#666666")
    
    def create_additional_options(self, parent):
        """Cria opções adicionais e seletor de imagens"""
        options_frame = tk.Frame(parent, bg="white")
        options_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        # Título
        tk.Label(options_frame, text="Imagens selecionadas", 
                font=("Arial", 10, "bold"), bg="white").pack(anchor=tk.W, pady=(0, 10))
        
        # Listbox com scroll
        scrollbar = ttk.Scrollbar(options_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.image_listbox = tk.Listbox(options_frame, width=25, height=10,
                                       yscrollcommand=scrollbar.set)
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.image_listbox.yview)
        
        # Adicionar itens de exemplo
        self.image_listbox.insert(0, "Foto de página inteira")
        self.image_listbox.insert(1, "13 x 18 cm. (2)")
        self.image_listbox.insert(2, "20 x 25 cm. (1)")
        
        # Botões de controle
        button_frame = tk.Frame(options_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="Adicionar...", width=12).pack(padx=5, pady=2)
        tk.Button(button_frame, text="Remover", width=12).pack(padx=5, pady=2)
    
    def create_bottom_controls(self, parent):
        """Cria controles inferiores (cópias, etc)"""
        control_frame = tk.Frame(parent, bg="white")
        control_frame.pack(fill=tk.X)
        
        # Cópias
        tk.Label(control_frame, text="Cópias de cada imagem:", bg="white").pack(side=tk.LEFT)
        
        spinbox = tk.Spinbox(control_frame, from_=1, to=10, textvariable=self.copies_var,
                            width=5)
        spinbox.pack(side=tk.LEFT, padx=10)
        
        # Checkbox
        self.adjust_var = tk.BooleanVar()
        tk.Checkbutton(control_frame, text="Ajustar imagem ao quadro",
                      variable=self.adjust_var, bg="white").pack(side=tk.LEFT, padx=10)
    
    def create_buttons(self, parent):
        """Cria botões de ação"""
        # Botão de opções
        tk.Button(parent, text="Opções...", width=12, relief=tk.RAISED).pack(side=tk.LEFT, padx=5)
        
        # Espaço elástico
        spacer = tk.Frame(parent, bg="white")
        spacer.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botões de ação
        tk.Button(parent, text="Imprimir", width=12, bg="#0066CC", 
                 fg="white", relief=tk.RAISED, command=self.print_action).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(parent, text="Cancelar", width=12, relief=tk.RAISED,
                 command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def print_action(self):
        """Ação de impressão"""
        config = f"""
Configuração de Impressão:
═════════════════════════
Impressora: {self.printer_var.get()}
Tamanho do papel: {self.paper_size_var.get()}
Qualidade: {self.quality_var.get()}
Tipo de papel: {self.paper_type_var.get()}
Cópias por imagem: {self.copies_var.get()}
Ajustar ao quadro: {'Sim' if self.adjust_var.get() else 'Não'}
"""
        messagebox.showinfo("Imprimindo", config + "\n✓ Impressão iniciada!")

def main():
    root = tk.Tk()
    app = PrintDialog(root)
    root.mainloop()

if __name__ == "__main__":
    main()
