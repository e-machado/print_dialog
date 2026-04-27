#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print Dialog com Integração CUPS
Exemplo avançado com suporte a impressoras reais via CUPS
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os

try:
    import cups
    CUPS_AVAILABLE = True
except ImportError:
    CUPS_AVAILABLE = False
    print("⚠ Aviso: python3-cups não está instalado")
    print("  Para usar integração CUPS: pip3 install pycups")

class CUPSPrintDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Imprimir - Integração CUPS")
        self.geometry("900x650")
        self.resizable(False, False)
        
        # Variáveis
        self.printers_list = []
        self.selected_files = []
        
        # Tentar conectar ao CUPS
        if CUPS_AVAILABLE:
            try:
                self.cups_conn = cups.Connection()
                self.get_available_printers()
            except Exception as e:
                messagebox.warning("Aviso CUPS", 
                    f"Não foi possível conectar ao CUPS:\n{str(e)}\n\n"
                    "O programa funcionará em modo simulação.")
                self.cups_conn = None
        else:
            self.cups_conn = None
        
        self.setup_ui()
        
    def get_available_printers(self):
        """Obtém lista de impressoras disponíveis do CUPS"""
        try:
            printers = self.cups_conn.getPrinters()
            self.printers_list = list(printers.keys())
            return self.printers_list
        except Exception as e:
            print(f"Erro ao obter impressoras: {e}")
            return []
    
    def setup_ui(self):
        """Configura a interface"""
        
        # Frame superior
        header = tk.Frame(self, bg="#0066CC", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="📄 Imprimir Imagens (CUPS Integration)",
                        font=("Arial", 11, "bold"), fg="white", bg="#0066CC")
        title.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Frame principal
        main = tk.Frame(self, bg="white")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Seção de opções
        self.create_options_section(main)
        
        # Separador
        sep = ttk.Separator(main, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=10)
        
        # Seção de conteúdo
        self.create_content_section(main)
        
        # Frame de rodapé
        footer = tk.Frame(self, bg="white")
        footer.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.create_footer(footer)
    
    def create_options_section(self, parent):
        """Cria opções de impressão"""
        opt_frame = tk.Frame(parent, bg="white")
        opt_frame.pack(fill=tk.X, pady=10)
        
        # Impressora
        tk.Label(opt_frame, text="Impressora:", bg="white", 
                width=20, anchor=tk.W).grid(row=0, column=0, padx=5)
        
        self.printer_var = tk.StringVar()
        
        if CUPS_AVAILABLE and self.printers_list:
            self.printer_var.set(self.printers_list[0])
            printers = self.printers_list
        else:
            self.printer_var.set("Nenhuma impressora disponível")
            printers = ["Simulação de Impressora", "Impressora Virtual 1", 
                       "Impressora Virtual 2"]
        
        printer_combo = ttk.Combobox(opt_frame, textvariable=self.printer_var,
                                     values=printers, state="readonly", width=30)
        printer_combo.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        # Papel
        tk.Label(opt_frame, text="Tamanho do papel:", bg="white",
                width=20, anchor=tk.W).grid(row=0, column=2, padx=5)
        
        self.paper_var = tk.StringVar(value="A4")
        paper_combo = ttk.Combobox(opt_frame, textvariable=self.paper_var,
                                   values=["A3", "A4", "A5", "Ofício"], 
                                   state="readonly", width=15)
        paper_combo.grid(row=0, column=3, padx=5, sticky=tk.EW)
        
        opt_frame.columnconfigure(1, weight=1)
        opt_frame.columnconfigure(3, weight=1)
    
    def create_content_section(self, parent):
        """Cria seção de conteúdo"""
        content = tk.Frame(parent, bg="white")
        content.pack(fill=tk.BOTH, expand=True)
        
        # Esquerda - Preview
        left = tk.Frame(content, bg="white")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        preview_label = tk.Label(left, text="Preview",
                               font=("Arial", 9, "bold"), bg="white")
        preview_label.pack(anchor=tk.W)
        
        self.preview_canvas = tk.Canvas(left, bg="#F5F5F5", 
                                        relief=tk.SUNKEN, height=300)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_canvas.create_text(250, 150, 
                                       text="Nenhuma imagem selecionada",
                                       font=("Arial", 11), fill="#999")
        
        # Direita - Lista de arquivos
        right = tk.Frame(content, bg="white", width=250)
        right.pack(side=tk.RIGHT, fill=tk.BOTH)
        right.pack_propagate(False)
        
        files_label = tk.Label(right, text="Arquivos",
                             font=("Arial", 9, "bold"), bg="white")
        files_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(right, width=30,
                                       yscrollcommand=scrollbar.set)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Botões
        btn_frame = tk.Frame(right, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Adicionar", width=14,
                 command=self.add_files).pack(pady=2)
        tk.Button(btn_frame, text="Remover", width=14,
                 command=self.remove_file).pack(pady=2)
        
        # Cópias
        copies_frame = tk.Frame(right, bg="white")
        copies_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(copies_frame, text="Cópias:", bg="white").pack(anchor=tk.W)
        
        self.copies_var = tk.StringVar(value="1")
        spin = tk.Spinbox(copies_frame, from_=1, to=10,
                         textvariable=self.copies_var, width=5)
        spin.pack(anchor=tk.W)
    
    def create_footer(self, parent):
        """Cria rodapé com botões"""
        tk.Button(parent, text="Configurações de Impressora", width=25,
                 command=self.show_printer_settings).pack(side=tk.LEFT, padx=5)
        
        parent.pack_propagate(False)
        
        tk.Button(parent, text="Cancelar", width=12,
                 command=self.quit).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(parent, text="Imprimir", width=12,
                 bg="#0066CC", fg="white",
                 command=self.print_action).pack(side=tk.RIGHT, padx=5)
    
    def add_files(self):
        """Adiciona arquivos para impressão"""
        files = filedialog.askopenfilenames(
            title="Selecionar imagens",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp"),
                      ("Todos", "*.*")]
        )
        
        for file in files:
            self.selected_files.append(file)
            self.files_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_file(self):
        """Remove arquivo selecionado"""
        sel = self.files_listbox.curselection()
        if sel:
            idx = sel[0]
            self.files_listbox.delete(idx)
            del self.selected_files[idx]
    
    def show_printer_settings(self):
        """Mostra configurações da impressora"""
        if not CUPS_AVAILABLE:
            messagebox.showinfo("Informação",
                "CUPS não está disponível.\n"
                "Instale com: pip3 install pycups")
            return
        
        if not self.cups_conn:
            messagebox.showwarning("Aviso",
                "Não foi possível conectar ao servidor CUPS.\n"
                "Verifique se está instalado e em execução.")
            return
        
        try:
            printer = self.printer_var.get()
            info = self.cups_conn.getPrinterAttributes(printer)
            
            msg = f"Impressora: {printer}\n\n"
            msg += f"Estado: {info.get('printer-state', 'Desconhecido')}\n"
            msg += f"Localização: {info.get('printer-location', 'N/A')}\n"
            msg += f"Descrição: {info.get('printer-info', 'N/A')}\n"
            
            messagebox.showinfo("Configurações da Impressora", msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter informações:\n{e}")
    
    def print_action(self):
        """Realiza a impressão"""
        printer = self.printer_var.get()
        copies = int(self.copies_var.get())
        paper = self.paper_var.get()
        
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
        
        if CUPS_AVAILABLE and self.cups_conn and printer != "Nenhuma impressora disponível":
            self.print_with_cups(printer, copies)
        else:
            self.print_simulation(printer, copies, paper)
    
    def print_with_cups(self, printer, copies):
        """Imprime via CUPS"""
        try:
            for file in self.selected_files:
                job_id = self.cups_conn.printFile(
                    printer,
                    file,
                    f"Print Job - {os.path.basename(file)}",
                    {"copies": str(copies)}
                )
                
            messagebox.showinfo("Sucesso",
                f"✓ Impressão enviada!\n"
                f"Impressora: {printer}\n"
                f"Arquivos: {len(self.selected_files)}\n"
                f"Cópias: {copies}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir:\n{e}")
    
    def print_simulation(self, printer, copies, paper):
        """Simula impressão quando CUPS não está disponível"""
        msg = f"""
✓ SIMULAÇÃO DE IMPRESSÃO
═══════════════════════════════════════

Impressora: {printer}
Tamanho do papel: {paper}
Cópias: {copies}

Arquivos para impressão:
───────────────────────────────────────
"""
        for i, file in enumerate(self.selected_files, 1):
            msg += f"{i}. {os.path.basename(file)}\n"
        
        msg += """
═══════════════════════════════════════
Status: Pronto para impressão
        """
        
        messagebox.showinfo("Impressão Simulada", msg)

def main():
    app = CUPSPrintDialog()
    app.mainloop()

if __name__ == "__main__":
    main()
