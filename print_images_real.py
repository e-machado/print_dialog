#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print Dialog Funcional
Carrega impressoras CUPS reais, imagens da pasta atual, 
mostra preview do layout e envia para impressão
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys
from pathlib import Path
from io import BytesIO
import traceback

# Tentar importar dependências
try:
    import cups
    CUPS_AVAILABLE = True
except ImportError:
    CUPS_AVAILABLE = False
    print("⚠ Aviso: pycups não está instalado")
    print("  Instale com: sudo apt-get install python3-cups ou pip3 install pycups")

try:
    from reportlab.lib.pagesizes import A4, A3, A5, letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas as reportlab_canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠ Aviso: reportlab não está instalado")
    print("  Instale com: pip3 install reportlab")

class ImagePrintDialog:
    def __init__(self, root, image_path=None):
        self.root = root
        self.root.title("Imprimir Imagens")
        self.root.geometry("1200x750")
        
        self.image_path = image_path
        
        if self.image_path:
           self.load_single_image(self.image_path)
       else:
           self.load_images_from_folder()


        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variáveis
        self.selected_images = []
        self.preview_images = {}
        self.cups_conn = None
        self.printers = []
        
        # Tentar conectar ao CUPS
        self.connect_cups()
        
        # Setup UI
        self.setup_ui()
        
        # Carregar imagens da pasta atual
        self.load_images_from_folder()
    
    def connect_cups(self):
        """Conecta ao CUPS e obtém lista de impressoras"""
        if not CUPS_AVAILABLE:
            return
        
        try:
            self.cups_conn = cups.Connection()
            printers_dict = self.cups_conn.getPrinters()
            self.printers = list(printers_dict.keys())
            print(f"✓ CUPS conectado. Impressoras encontradas: {self.printers}")
        except Exception as e:
            print(f"✗ Erro ao conectar CUPS: {e}")
            self.cups_conn = None
            self.printers = []
    
    def load_images_from_folder(self):
        """Carrega imagens da pasta atual"""
        current_dir = os.getcwd()
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
        
        print(f"Procurando imagens em: {current_dir}")
        
        try:
            for file in sorted(os.listdir(current_dir)):
                if os.path.splitext(file)[1].lower() in image_extensions:
                    full_path = os.path.join(current_dir, file)
                    self.selected_images.append({
                        'path': full_path,
                        'name': file,
                        'copies': 1
                    })
                    print(f"  ✓ Encontrada: {file}")
        except Exception as e:
            print(f"✗ Erro ao carregar imagens: {e}")
        
        # Atualizar interface
        self.update_images_list()
        self.update_preview()

    def load_single_image(self, image_path):
        """Carrega uma única imagem especificada"""
        
        # Verificar existência
        if not os.path.exists(image_path):
            messagebox.showerror("Erro", f"Arquivo não encontrado...")
            return
        
        # Verificar extensão
        if os.path.splitext(image_path)[1].lower() not in image_extensions:
            messagebox.showerror("Erro", f"Formato não suportado...")
            return
        
        # Adicionar à lista
        self.selected_images.append({
            'path': os.path.abspath(image_path),
            'name': os.path.basename(image_path),
            'copies': 1
        })
        
        # Atualizar interface
        self.update_images_list()
        self.update_preview()



    def setup_ui(self):
        """Configura toda a interface"""
        
        # Header
        header = tk.Frame(self.root, bg="#0066CC", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="📄 Imprimir Imagens - Sistema Real de Impressão",
                        font=("Arial", 12, "bold"), fg="white", bg="#0066CC")
        title.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Main content
        main = tk.Frame(self.root, bg="white")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Options
        left_panel = tk.Frame(main, bg="white", width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_options_panel(left_panel)
        
        # Right panel - Preview
        right_panel = tk.Frame(main, bg="white")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_preview_panel(right_panel)
        
        # Footer
        footer = tk.Frame(self.root, bg="white")
        footer.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.create_footer(footer)
    
    def create_options_panel(self, parent):
        """Cria painel de opções"""
        
        # Impressora
        tk.Label(parent, text="Impressora:", font=("Arial", 9, "bold"),
                bg="white").pack(anchor=tk.W, pady=(0, 5))
        
        self.printer_var = tk.StringVar()
        if self.printers:
            self.printer_var.set(self.printers[0])
            printers_list = self.printers
        else:
            self.printer_var.set("Nenhuma impressora")
            printers_list = ["Simular (PDF)"]
        
        self.printer_combo = ttk.Combobox(parent, textvariable=self.printer_var,
                                         values=printers_list, state="readonly")
        self.printer_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Tamanho do papel
        tk.Label(parent, text="Tamanho Papel:", font=("Arial", 9, "bold"),
                bg="white").pack(anchor=tk.W, pady=(0, 5))
        
        self.paper_var = tk.StringVar(value="A4")
        self.paper_sizes = {
            "A4": (210, 297),      # mm
            "A3": (297, 420),
            "A5": (148, 210),
            "Carta": (216, 279),
        }
        
        paper_combo = ttk.Combobox(parent, textvariable=self.paper_var,
                                   values=list(self.paper_sizes.keys()),
                                   state="readonly")
        paper_combo.pack(fill=tk.X, pady=(0, 15))
        paper_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        
        # Qualidade
        tk.Label(parent, text="Qualidade:", font=("Arial", 9, "bold"),
                bg="white").pack(anchor=tk.W, pady=(0, 5))
        
        self.quality_var = tk.StringVar(value="Normal")
        quality_combo = ttk.Combobox(parent, textvariable=self.quality_var,
                                     values=["Rascunho", "Normal", "Alta"],
                                     state="readonly")
        quality_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Disposição
        tk.Label(parent, text="Disposição:", font=("Arial", 9, "bold"),
                bg="white").pack(anchor=tk.W, pady=(0, 5))
        
        self.layout_var = tk.StringVar(value="1x1")
        layout_combo = ttk.Combobox(parent, textvariable=self.layout_var,
                                    values=["1x1", "2x1", "2x2", "3x3"],
                                    state="readonly")
        layout_combo.pack(fill=tk.X, pady=(0, 15))
        layout_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        
        # Margens
        tk.Label(parent, text="Margem (mm):", font=("Arial", 9, "bold"),
                bg="white").pack(anchor=tk.W, pady=(0, 5))
        
        self.margin_var = tk.StringVar(value="10")
        margin_spin = tk.Spinbox(parent, from_=0, to=50, textvariable=self.margin_var,
                                width=10)
        margin_spin.pack(fill=tk.X, pady=(0, 15))
        
        # Separador
        sep = ttk.Separator(parent, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=10)
        
        # Lista de imagens
        tk.Label(parent, text="Imagens:", font=("Arial", 9, "bold"),
                bg="white").pack(anchor=tk.W, pady=(0, 5))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.images_listbox = tk.Listbox(parent, yscrollcommand=scrollbar.set,
                                        height=10, font=("Arial", 8))
        self.images_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.images_listbox.yview)
        self.images_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview())
        
        # Cópias para imagem selecionada
        copies_frame = tk.Frame(parent, bg="white")
        copies_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(copies_frame, text="Cópias:", font=("Arial", 8),
                bg="white").pack(side=tk.LEFT)
        
        self.copies_var = tk.StringVar(value="1")
        copies_spin = tk.Spinbox(copies_frame, from_=1, to=100,
                                textvariable=self.copies_var, width=5)
        copies_spin.pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Button(copies_frame, text="Atualizar", width=8,
                 command=self.update_selected_copies).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botões
        btn_frame = tk.Frame(parent, bg="white")
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(btn_frame, text="Adicionar", width=12,
                 command=self.add_images).pack(pady=2)
        tk.Button(btn_frame, text="Remover", width=12,
                 command=self.remove_image).pack(pady=2)
        tk.Button(btn_frame, text="Limpar Tudo", width=12,
                 command=self.clear_all).pack(pady=2)
    
    def create_preview_panel(self, parent):
        """Cria painel de preview"""
        
        # Info
        info_frame = tk.Frame(parent, bg="white")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="Preview de Impressão",
                font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT)
        
        self.info_label = tk.Label(info_frame, text="",
                                  font=("Arial", 8), fg="#666", bg="white")
        self.info_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Canvas de preview
        self.preview_canvas = tk.Canvas(parent, bg="white", relief=tk.SUNKEN,
                                       highlightthickness=1, highlightbackground="#ccc")
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Navegação
        nav_frame = tk.Frame(parent, bg="white")
        nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.page_label = tk.Label(nav_frame, text="Página 1",
                                   font=("Arial", 9), bg="white")
        self.page_label.pack(side=tk.LEFT)
        
        nav_frame.pack_propagate(False)
        nav_frame.configure(height=30)
        
        tk.Button(nav_frame, text="◀", width=2,
                 command=lambda: self.change_page(-1)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="▶", width=2,
                 command=lambda: self.change_page(1)).pack(side=tk.LEFT)
    
    def create_footer(self, parent):
        """Cria rodapé com botões"""
        
        tk.Button(parent, text="Visualizar PDF", width=15,
                 command=self.generate_pdf).pack(side=tk.LEFT, padx=5)
        
        parent.pack_propagate(False)
        parent.configure(height=40)
        
        tk.Button(parent, text="Cancelar", width=15,
                 command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(parent, text="Imprimir", width=15,
                 bg="#0066CC", fg="white",
                 command=self.print_action).pack(side=tk.RIGHT, padx=5)
    
    def update_images_list(self):
        """Atualiza listbox de imagens"""
        self.images_listbox.delete(0, tk.END)
        
        for i, img in enumerate(self.selected_images):
            display_text = f"{img['name']} ({img['copies']}x)"
            self.images_listbox.insert(tk.END, display_text)
    
    def update_selected_copies(self):
        """Atualiza número de cópias da imagem selecionada"""
        sel = self.images_listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma imagem")
            return
        
        idx = sel[0]
        try:
            copies = int(self.copies_var.get())
            if copies > 0:
                self.selected_images[idx]['copies'] = copies
                self.update_images_list()
                self.update_preview()
        except ValueError:
            messagebox.showerror("Erro", "Número de cópias inválido")
    
    def update_preview(self):
        """Atualiza preview das imagens na disposição"""
        if not self.selected_images:
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(
                self.preview_canvas.winfo_width()/2,
                self.preview_canvas.winfo_height()/2,
                text="Nenhuma imagem selecionada",
                font=("Arial", 12), fill="#999"
            )
            return
        
        # Obter layout
        layout_str = self.layout_var.get()
        cols, rows = map(int, layout_str.split("x"))
        
        # Limpar canvas
        self.preview_canvas.delete("all")
        
        # Desenhar fundo
        self.preview_canvas.create_rectangle(
            0, 0,
            self.preview_canvas.winfo_width(),
            self.preview_canvas.winfo_height(),
            fill="white", outline="#ccc"
        )
        
        # Calcular tamanho de cada célula
        margin = int(self.margin_var.get()) * 2  # pixels
        canvas_w = self.preview_canvas.winfo_width() - margin
        canvas_h = self.preview_canvas.winfo_height() - margin
        
        cell_w = canvas_w / cols
        cell_h = canvas_h / rows
        
        # Obter todas as imagens com cópias repetidas
        all_images = []
        for img_data in self.selected_images:
            for _ in range(img_data['copies']):
                all_images.append(img_data)
        
        # Calcular número de páginas
        images_per_page = cols * rows
        total_pages = (len(all_images) + images_per_page - 1) // images_per_page
        self.current_page = getattr(self, 'current_page', 0)
        
        if self.current_page >= total_pages:
            self.current_page = 0
        
        # Atualizar label de página
        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")
        
        # Desenhar imagens da página atual
        start_idx = self.current_page * images_per_page
        end_idx = min(start_idx + images_per_page, len(all_images))
        
        for pos, img_idx in enumerate(range(start_idx, end_idx)):
            row = pos // cols
            col = pos % cols
            
            x = int(margin/2 + col * cell_w + 5)
            y = int(margin/2 + row * cell_h + 5)
            w = int(cell_w - 10)
            h = int(cell_h - 10)
            
            # Desenhar borda
            self.preview_canvas.create_rectangle(
                x, y, x + w, y + h,
                outline="#ddd", width=1
            )
            
            # Carregar e desenhar imagem
            try:
                img = Image.open(all_images[img_idx]['path'])
                img.thumbnail((w - 10, h - 10), Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(img)
                self.preview_images[img_idx] = photo  # Manter referência
                
                img_x = x + (w - photo.width()) // 2
                img_y = y + (h - photo.height()) // 2
                
                self.preview_canvas.create_image(
                    img_x, img_y,
                    image=photo,
                    anchor=tk.NW
                )
                
                # Nome da imagem
                self.preview_canvas.create_text(
                    x + 5, y + h - 15,
                    text=all_images[img_idx]['name'][:20],
                    font=("Arial", 7),
                    anchor=tk.SW,
                    fill="#666"
                )
            except Exception as e:
                self.preview_canvas.create_text(
                    x + w/2, y + h/2,
                    text=f"Erro: {str(e)[:30]}",
                    font=("Arial", 7),
                    fill="red"
                )
        
        # Atualizar info
        total_copies = sum(img['copies'] for img in self.selected_images)
        self.info_label.config(
            text=f"Total: {len(self.selected_images)} imagens | "
                 f"{total_copies} cópias | {total_pages} página(s)"
        )
    
    def change_page(self, direction):
        """Muda página do preview"""
        layout_str = self.layout_var.get()
        cols, rows = map(int, layout_str.split("x"))
        images_per_page = cols * rows
        
        # Contar total de imagens com cópias
        all_images_count = sum(img['copies'] for img in self.selected_images)
        total_pages = (all_images_count + images_per_page - 1) // images_per_page
        
        self.current_page = getattr(self, 'current_page', 0) + direction
        
        if self.current_page < 0:
            self.current_page = total_pages - 1
        elif self.current_page >= total_pages:
            self.current_page = 0
        
        self.update_preview()
    
    def add_images(self):
        """Adiciona imagens"""
        files = filedialog.askopenfilenames(
            title="Selecionar Imagens",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                      ("Todos", "*.*")]
        )
        
        for file in files:
            # Verificar se já existe
            if not any(img['path'] == file for img in self.selected_images):
                self.selected_images.append({
                    'path': file,
                    'name': os.path.basename(file),
                    'copies': 1
                })
        
        self.update_images_list()
        self.update_preview()
    
    def remove_image(self):
        """Remove imagem selecionada"""
        sel = self.images_listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma imagem")
            return
        
        idx = sel[0]
        del self.selected_images[idx]
        self.update_images_list()
        self.update_preview()
    
    def clear_all(self):
        """Limpa todas as imagens"""
        if messagebox.askyesno("Confirmar", "Remover todas as imagens?"):
            self.selected_images = []
            self.update_images_list()
            self.update_preview()
    
    def generate_pdf(self):
        """Gera PDF com as imagens para visualização"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Erro", 
                "reportlab não está instalado.\n"
                "Instale com: pip3 install reportlab")
            return
        
        if not self.selected_images:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada")
            return
        
        try:
            # Abrir diálogo para salvar
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf"), ("Todos", "*.*")],
                initialfile="impressao.pdf"
            )
            
            if not filename:
                return
            
            # Obter layout
            layout_str = self.layout_var.get()
            cols, rows = map(int, layout_str.split("x"))
            
            # Tamanho do papel
            paper_size = self.paper_sizes[self.paper_var.get()]
            if self.paper_var.get() == "A4":
                from reportlab.lib.pagesizes import A4
                pagesize = A4
            elif self.paper_var.get() == "A3":
                from reportlab.lib.pagesizes import A3
                pagesize = A3
            elif self.paper_var.get() == "A5":
                from reportlab.lib.pagesizes import A5
                pagesize = A5
            else:  # Carta
                from reportlab.lib.pagesizes import letter
                pagesize = letter
            
            # Margem em pixels
            margin_mm = int(self.margin_var.get())
            from reportlab.lib.units import mm
            margin = margin_mm * mm
            
            # Criar PDF
            c = reportlab_canvas.Canvas(filename, pagesize=pagesize)
            page_width, page_height = pagesize
            
            # Calcular dimensões das células
            cell_width = (page_width - 2 * margin) / cols
            cell_height = (page_height - 2 * margin) / rows
            
            # Obter todas as imagens com cópias
            all_images = []
            for img_data in self.selected_images:
                for _ in range(img_data['copies']):
                    all_images.append(img_data['path'])
            
            # Desenhar imagens
            images_per_page = cols * rows
            total_pages = (len(all_images) + images_per_page - 1) // images_per_page
            
            for page_num in range(total_pages):
                start_idx = page_num * images_per_page
                end_idx = min(start_idx + images_per_page, len(all_images))
                
                # Desenhar imagens desta página
                for pos in range(start_idx, end_idx):
                    row = (pos - start_idx) // cols
                    col = (pos - start_idx) % cols
                    
                    x = margin + col * cell_width
                    y = page_height - margin - (row + 1) * cell_height
                    
                    try:
                        img = Image.open(all_images[pos])
                        # Calcular tamanho mantendo proporção
                        img_w = cell_width - 10 * mm
                        img_h = cell_height - 10 * mm
                        
                        w, h = img.size
                        ratio = min(img_w / w, img_h / h)
                        new_w = int(w * ratio)
                        new_h = int(h * ratio)
                        
                        # Centralizar imagem na célula
                        img_x = x + (cell_width - new_w) / 2
                        img_y = y + (cell_height - new_h) / 2
                        
                        c.drawImage(all_images[pos], img_x, img_y,
                                   width=new_w, height=new_h)
                    except Exception as e:
                        c.drawString(x + 10, y + 10, f"Erro: {str(e)[:30]}")
                
                # Nova página se não for a última
                if page_num < total_pages - 1:
                    c.showPage()
            
            c.save()
            messagebox.showinfo("Sucesso", 
                f"PDF gerado com sucesso!\n{filename}")
            
            # Abrir PDF
            os.system(f'xdg-open "{filename}" 2>/dev/null &')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF:\n{e}")
            traceback.print_exc()
    
    def print_action(self):
        """Realiza a impressão"""
        if not self.selected_images:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada")
            return
        
        printer = self.printer_var.get()
        
        if printer == "Nenhuma impressora" or printer == "Simular (PDF)":
            messagebox.showinfo("Simulação",
                "Gerando PDF para visualização...\n"
                "Use 'Visualizar PDF' para ver o resultado final")
            self.generate_pdf()
            return
        
        # Impressão real via CUPS
        if not CUPS_AVAILABLE or not self.cups_conn:
            messagebox.showerror("Erro", 
                "CUPS não está disponível.\n"
                "Instale com: sudo apt-get install python3-cups")
            return
        
        try:
            # Gerar PDF temporário
            import tempfile
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp_path = tmp.name
            
            # Usar a função de geração de PDF
            self.generate_pdf_temp(tmp_path)
            
            # Enviar para impressora
            job_id = self.cups_conn.printFile(
                printer,
                tmp_path,
                "Impressão de Imagens",
                {
                    "media": self.paper_var.get(),
                    "print-quality": self.quality_var.get()
                }
            )
            
            messagebox.showinfo("Sucesso",
                f"✓ Impressão enviada!\n"
                f"Impressora: {printer}\n"
                f"Job ID: {job_id}")
            
            # Limpar arquivo temporário
            import atexit
            atexit.register(lambda: os.unlink(tmp_path) if os.path.exists(tmp_path) else None)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir:\n{e}")
            traceback.print_exc()
    
    def generate_pdf_temp(self, filename):
        """Gera PDF temporário (usado internamente)"""
        if not REPORTLAB_AVAILABLE:
            raise Exception("reportlab não está instalado")
        
        # Similar a generate_pdf mas sem diálogo
        layout_str = self.layout_var.get()
        cols, rows = map(int, layout_str.split("x"))
        
        if self.paper_var.get() == "A4":
            from reportlab.lib.pagesizes import A4
            pagesize = A4
        elif self.paper_var.get() == "A3":
            from reportlab.lib.pagesizes import A3
            pagesize = A3
        elif self.paper_var.get() == "A5":
            from reportlab.lib.pagesizes import A5
            pagesize = A5
        else:
            from reportlab.lib.pagesizes import letter
            pagesize = letter
        
        margin_mm = int(self.margin_var.get())
        from reportlab.lib.units import mm
        margin = margin_mm * mm
        
        c = reportlab_canvas.Canvas(filename, pagesize=pagesize)
        page_width, page_height = pagesize
        
        cell_width = (page_width - 2 * margin) / cols
        cell_height = (page_height - 2 * margin) / rows
        
        all_images = []
        for img_data in self.selected_images:
            for _ in range(img_data['copies']):
                all_images.append(img_data['path'])
        
        images_per_page = cols * rows
        total_pages = (len(all_images) + images_per_page - 1) // images_per_page
        
        for page_num in range(total_pages):
            start_idx = page_num * images_per_page
            end_idx = min(start_idx + images_per_page, len(all_images))
            
            for pos in range(start_idx, end_idx):
                row = (pos - start_idx) // cols
                col = (pos - start_idx) % cols
                
                x = margin + col * cell_width
                y = page_height - margin - (row + 1) * cell_height
                
                try:
                    img = Image.open(all_images[pos])
                    img_w = cell_width - 10 * mm
                    img_h = cell_height - 10 * mm
                    
                    w, h = img.size
                    ratio = min(img_w / w, img_h / h)
                    new_w = int(w * ratio)
                    new_h = int(h * ratio)
                    
                    img_x = x + (cell_width - new_w) / 2
                    img_y = y + (cell_height - new_h) / 2
                    
                    c.drawImage(all_images[pos], img_x, img_y,
                               width=new_w, height=new_h)
                except:
                    pass
            
            if page_num < total_pages - 1:
                c.showPage()
        
        c.save()

def main():
    # Novo: processar argumentos de linha de comando
    image_path = None
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    root = tk.Tk()
    app = ImagePrintDialog(root, image_path=image_path)
    root.mainloop()


#def main():
#    root = tk.Tk()
#    app = ImagePrintDialog(root)
#    root.mainloop()

if __name__ == "__main__":
    main()
