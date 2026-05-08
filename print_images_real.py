#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Impressão de Imagens
UI: 1.py  |  Backend: 2.py  |  Layout: grid (header/content/footer sempre visíveis)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys
import json
import traceback

# ── Dependências opcionais ────────────────────────────────────────────────────
try:
    import cups
    CUPS_AVAILABLE = True
except ImportError:
    CUPS_AVAILABLE = False
    print("⚠ pycups não instalado: sudo apt-get install python3-cups")

try:
    from reportlab.lib.pagesizes import A4, A3, A5, letter
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as reportlab_canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠ reportlab não instalado: pip3 install reportlab")

# ── Temas ─────────────────────────────────────────────────────────────────────
THEMES = {
    'light': {
        'bg':             '#ffffff',
        'panel_bg':       '#f5f5f5',
        'fg':             '#333333',
        'fg_secondary':   '#666666',
        'header_bg':      '#0066CC',
        'header_fg':      '#ffffff',
        'canvas_bg':      '#e0e0e0',
        'listbox_bg':     '#ffffff',
        'listbox_fg':     '#333333',
        'btn_bg':         '#e0e0e0',
        'btn_fg':         '#333333',
        'primary_btn_bg': '#0066CC',
        'primary_btn_fg': '#ffffff',
        'border':         '#cccccc',
        'preview_paper':  '#ffffff',
        'preview_text':   '#333333',
        'theme_btn_text': '🌙 Escuro',
        'spinbox_bg':     '#ffffff',
        'spinbox_fg':     '#333333',
    },
    'dark': {
        'bg':             '#1e1e2e',
        'panel_bg':       '#181825',
        'fg':             '#cdd6f4',
        'fg_secondary':   '#a6adc8',
        'header_bg':      '#11111b',
        'header_fg':      '#cdd6f4',
        'canvas_bg':      '#313244',
        'listbox_bg':     '#1e1e2e',
        'listbox_fg':     '#cdd6f4',
        'btn_bg':         '#45475a',
        'btn_fg':         '#cdd6f4',
        'primary_btn_bg': '#89b4fa',
        'primary_btn_fg': '#1e1e2e',
        'border':         '#313244',
        'preview_paper':  '#313244',
        'preview_text':   '#cdd6f4',
        'theme_btn_text': '☀ Claro',
        'spinbox_bg':     '#1e1e2e',
        'spinbox_fg':     '#cdd6f4',
    },
}

CONFIG_FILE = "print_config.json"


class ImagePrintDialog:
    def __init__(self, root, image_path=None):
        self.root = root
        self.root.title("Imprimir Imagens Pro")

        # Persistência + tema
        self.current_theme = self.load_config().get('theme', 'light')
        self._tw = []   # [(widget, {prop: color_key})]

        # Tamanho responsivo
        try:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            ww = min(1100, int(sw * 0.82))
            wh = min(800,  int(sh * 0.82))
            self.root.geometry(f"{ww}x{wh}")
        except Exception:
            self.root.geometry("1000x680")

        self.root.minsize(700, 500)
        self.root.resizable(True, True)

        # Estado
        self.selected_images = []
        self.preview_images  = {}
        self.cups_conn       = None
        self.printers        = []
        self.image_path      = image_path
        self.current_page    = 0

        self.connect_cups()
        self.setup_ui()
        self._apply_theme()   # aplica tema após criar todos os widgets

        if self.image_path:
            self.load_single_image(self.image_path)
        else:
            self.load_images_from_folder()

    # ── Persistência ─────────────────────────────────────────────────────────
    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({'theme': self.current_theme}, f)
        except Exception:
            pass

    # ── Gerenciamento de tema ─────────────────────────────────────────────────
    def c(self, key: str) -> str:
        return THEMES[self.current_theme][key]

    def _reg(self, widget, **color_map):
        """Registra widget para recoloração ao trocar tema."""
        self._tw.append((widget, color_map))
        return widget

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_config()
        self._apply_theme()
        self.update_preview()

    def _apply_theme(self):
        colors = THEMES[self.current_theme]
        self.root.config(bg=colors['bg'])

        for widget, color_map in self._tw:
            try:
                cfg = {prop: colors[key] for prop, key in color_map.items()}
                # Corrige bordas e estados ativos conforme o tipo de widget
                if 'highlightbackground' in widget.keys():
                    cfg['highlightbackground'] = colors['border']
                if isinstance(widget, tk.Button):
                    cfg['activebackground'] = colors['btn_bg']
                    cfg['activeforeground'] = colors['fg']
                widget.config(**cfg)
            except Exception:
                pass

        try:
            self.theme_btn.config(text=self.c('theme_btn_text'))
        except Exception:
            pass

        self._update_ttk_styles()

    def _update_ttk_styles(self):
        style = ttk.Style()
        style.theme_use('default')  # base neutra, evita cores do sistema
        bg  = self.c('panel_bg')
        fg  = self.c('fg')
        sbg = self.c('spinbox_bg')
        bdr = self.c('border')

        style.configure('TCombobox',
                         fieldbackground=sbg, background=bg,
                         foreground=fg, arrowcolor=fg,
                         selectbackground=sbg, selectforeground=fg)
        style.map('TCombobox',
                  fieldbackground=[('readonly', sbg)],
                  foreground=[('readonly', fg)])
        style.configure('TSeparator', background=bdr)
        style.configure('TScrollbar',
                         background=self.c('btn_bg'),
                         troughcolor=self.c('canvas_bg'),
                         arrowcolor=fg)

    # =========================================================================
    # LAYOUT PRINCIPAL — grid no root garante footer/header sempre visíveis
    #
    #   row 0 │ header       (altura fixa, grid_propagate=False)
    #   row 1 │ PanedWindow  (weight=1, expande livremente)
    #   row 2 │ footer       (altura fixa, grid_propagate=False)
    # =========================================================================
    def setup_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ── Header (row 0) ────────────────────────────────────────────────────
        header = self._reg(tk.Frame(self.root, height=50), bg='header_bg')
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)  # espaço elástico no meio

        self._reg(
            tk.Label(header, text="📄 Sistema de Impressão",
                     font=("Arial", 11, "bold")),
            fg='header_fg', bg='header_bg'
        ).grid(row=0, column=0, padx=15, pady=12, sticky='w')

        self.theme_btn = self._reg(
            tk.Button(header, font=("Arial", 9), relief=tk.FLAT,
                      cursor="hand2", command=self.toggle_theme, padx=10),
            bg='header_bg', fg='header_fg'
        )
        self.theme_btn.grid(row=0, column=2, padx=15, pady=10, sticky='e')

        # ── Área central (row 1) — PanedWindow redimensionável ────────────────
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.grid(row=1, column=0, sticky='nsew', padx=6, pady=4)

        # Painel esquerdo
        left = self._reg(tk.Frame(paned, width=280), bg='panel_bg')
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)
        paned.add(left, weight=0)
        self.create_options_panel(left)

        # Painel direito
        right = self._reg(tk.Frame(paned), bg='bg')
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)
        paned.add(right, weight=1)
        self.create_preview_panel(right)

        # ── Footer (row 2) — sempre visível por estar fixo no grid ───────────
        footer = self._reg(tk.Frame(self.root, height=48), bg='bg')
        footer.grid(row=2, column=0, sticky='ew', padx=8, pady=(2, 6))
        footer.grid_propagate(False)
        self.create_footer(footer)

    # =========================================================================
    # PAINEL DE OPÇÕES — canvas scrollável com grid (scrollbar nunca some)
    # =========================================================================
    def create_options_panel(self, parent):
        # grid: canvas col 0, scrollbar col 1 — ambos visíveis sempre
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        vscroll = ttk.Scrollbar(parent, orient=tk.VERTICAL)
        vscroll.grid(row=0, column=1, sticky='ns')

        canvas = self._reg(tk.Canvas(parent, highlightthickness=0), bg='panel_bg')
        canvas.grid(row=0, column=0, sticky='nsew')
        canvas.configure(yscrollcommand=vscroll.set)
        vscroll.configure(command=canvas.yview)

        scroll_frame = self._reg(tk.Frame(canvas), bg='panel_bg')
        win_id = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

        # Scrollregion acompanha conteúdo; largura acompanha canvas
        scroll_frame.bind('<Configure>',
                          lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda e: canvas.itemconfig(win_id, width=e.width))

        # Roda do mouse
        canvas.bind_all('<MouseWheel>',
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'))

        self.create_widgets_inside_scroll(scroll_frame)

    def create_widgets_inside_scroll(self, opts):
        """Todos os controles de impressão dentro do painel scrollável."""

        def sec(text):
            self._reg(
                tk.Label(opts, text=text, font=("Arial", 9, "bold")),
                bg='panel_bg', fg='fg'
            ).pack(anchor=tk.W, padx=8, pady=(10, 2))

        def combo(var, values, callback=None):
            cb = ttk.Combobox(opts, textvariable=var, values=values, state='readonly')
            cb.pack(fill=tk.X, padx=8, pady=(0, 6))
            if callback:
                cb.bind('<<ComboboxSelected>>', lambda e: callback())
            return cb

        # Impressora
        sec("Impressora:")
        self.printer_var = tk.StringVar()
        plist = self.printers if self.printers else ["Simular (PDF)"]
        self.printer_var.set(plist[0])
        combo(self.printer_var, plist)

        # Papel
        sec("Tamanho Papel:")
        self.paper_var   = tk.StringVar(value="A4")
        self.paper_sizes = {"A4": (210, 297), "A3": (297, 420),
                            "A5": (148, 210), "Carta": (216, 279)}
        combo(self.paper_var, list(self.paper_sizes.keys()), self.update_preview)

        # Orientação
        sec("Orientação:")
        self.orientation_var = tk.StringVar(value="Retrato")
        combo(self.orientation_var, ["Retrato", "Paisagem"], self.update_preview)

        # Qualidade
        sec("Qualidade:")
        self.quality_var = tk.StringVar(value="Normal")
        combo(self.quality_var, ["Rascunho", "Normal", "Alta"])

        # Disposição
        sec("Disposição:")
        self.layout_var = tk.StringVar(value="1x1")
        combo(self.layout_var, ["1x1", "2x1", "2x2", "3x3"], self.update_preview)

        # Margem
        sec("Margem (mm):")
        self.margin_var = tk.StringVar(value="10")
        self._reg(
            tk.Spinbox(opts, from_=0, to=50, textvariable=self.margin_var,
                       command=self.update_preview),
            bg='spinbox_bg', fg='spinbox_fg'
        ).pack(fill=tk.X, padx=8, pady=(0, 6))

        ttk.Separator(opts, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=8)

        # Lista de imagens
        sec("Imagens:")
        list_frame = self._reg(tk.Frame(opts), bg='panel_bg')
        list_frame.pack(fill=tk.X, padx=8)

        # Scrollbar da lista antes do Listbox no pack (garante espaço)
        sb_list = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        sb_list.pack(side=tk.RIGHT, fill=tk.Y)

        self.images_listbox = self._reg(
            tk.Listbox(list_frame, yscrollcommand=sb_list.set,
                       height=6, font=("Arial", 8),
                       relief=tk.FLAT, highlightthickness=1),
            bg='listbox_bg', fg='listbox_fg',
            selectbackground='primary_btn_bg', selectforeground='primary_btn_fg',
            highlightbackground='border'
        )
        self.images_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sb_list.configure(command=self.images_listbox.yview)
        self.images_listbox.bind('<<ListboxSelect>>', lambda e: self.update_preview())

        # Cópias
        cf = self._reg(tk.Frame(opts), bg='panel_bg')
        cf.pack(fill=tk.X, padx=8, pady=(6, 0))

        self._reg(
            tk.Label(cf, text="Cópias:", font=("Arial", 8)),
            bg='panel_bg', fg='fg'
        ).pack(side=tk.LEFT)

        self.copies_var = tk.StringVar(value="1")
        self._reg(
            tk.Spinbox(cf, from_=1, to=100, textvariable=self.copies_var, width=5),
            bg='spinbox_bg', fg='spinbox_fg'
        ).pack(side=tk.LEFT, padx=(4, 0))

        self._reg(
            tk.Button(cf, text="Atualizar", font=("Arial", 8),
                      command=self.update_selected_copies),
            bg='btn_bg', fg='btn_fg'
        ).pack(side=tk.RIGHT)

        # Botões da lista
        bf = self._reg(tk.Frame(opts), bg='panel_bg')
        bf.pack(fill=tk.X, padx=8, pady=(6, 10))

        for text, cmd in [("＋ Adicionar",  self.add_images),
                          ("🗑 Remover",    self.remove_image),
                          ("✖ Limpar Tudo", self.clear_all)]:
            self._reg(
                tk.Button(bf, text=text, anchor='w', font=("Arial", 8), command=cmd),
                bg='btn_bg', fg='btn_fg'
            ).pack(fill=tk.X, pady=2)

    # =========================================================================
    # PAINEL DE PREVIEW — info bar + canvas expansível + nav
    # =========================================================================
    def create_preview_panel(self, parent):
        # row 0: info bar  (fixa)
        # row 1: canvas    (expande)
        # row 2: nav       (fixa)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Info bar
        info_frame = self._reg(tk.Frame(parent), bg='bg')
        info_frame.grid(row=0, column=0, sticky='ew', pady=(2, 4))

        self._reg(
            tk.Label(info_frame, text="Preview de Impressão",
                     font=("Arial", 10, "bold")),
            bg='bg', fg='fg'
        ).pack(side=tk.LEFT)

        self.info_label = self._reg(
            tk.Label(info_frame, text="", font=("Arial", 8)),
            bg='bg', fg='fg_secondary'
        )
        self.info_label.pack(side=tk.LEFT, padx=10)

        # Canvas de preview
        self.preview_canvas = self._reg(
            tk.Canvas(parent, highlightthickness=1),
            bg='canvas_bg', highlightbackground='border'
        )
        self.preview_canvas.grid(row=1, column=0, sticky='nsew')

        # Barra de navegação
        nav_frame = self._reg(tk.Frame(parent), bg='bg')
        nav_frame.grid(row=2, column=0, sticky='ew', pady=(4, 2))

        self.page_label = self._reg(
            tk.Label(nav_frame, text="Página 1 de 1", font=("Arial", 9)),
            bg='bg', fg='fg'
        )
        self.page_label.pack(side=tk.LEFT)

        for text, delta in [("◀", -1), ("▶", 1)]:
            self._reg(
                tk.Button(nav_frame, text=text, width=3,
                          command=lambda d=delta: self.change_page(d)),
                bg='btn_bg', fg='btn_fg'
            ).pack(side=tk.LEFT, padx=3)

    # =========================================================================
    # FOOTER — grid_propagate=False garante altura fixa, nunca cortado
    # =========================================================================
    def create_footer(self, parent):
        parent.grid_columnconfigure(1, weight=1)  # espaço central elástico

        self._reg(
            tk.Button(parent, text="Visualizar PDF", command=self.generate_pdf),
            bg='btn_bg', fg='btn_fg'
        ).grid(row=0, column=0, padx=(4, 2), pady=8, sticky='w')

        # coluna 1 = espaço elástico

        self._reg(
            tk.Button(parent, text="Cancelar", width=12, command=self.root.quit),
            bg='btn_bg', fg='btn_fg'
        ).grid(row=0, column=2, padx=2, pady=8, sticky='e')

        self._reg(
            tk.Button(parent, text="🖨  Imprimir", font=("Arial", 10, "bold"),
                      width=14, command=self.print_action),
            bg='primary_btn_bg', fg='primary_btn_fg'
        ).grid(row=0, column=3, padx=(2, 4), pady=8, sticky='e')

    # =========================================================================
    # BACKEND — CUPS, imagens, preview, PDF, impressão  (de 2.py na íntegra)
    # =========================================================================

    # ── CUPS ──────────────────────────────────────────────────────────────────
    def connect_cups(self):
        if not CUPS_AVAILABLE:
            return
        try:
            self.cups_conn = cups.Connection()
            self.printers  = list(self.cups_conn.getPrinters().keys())
            print(f"✓ CUPS conectado. Impressoras: {self.printers}")
        except Exception as e:
            print(f"✗ Erro ao conectar CUPS: {e}")
            self.cups_conn = None
            self.printers  = []

    # ── Carregar imagens ──────────────────────────────────────────────────────
    def load_images_from_folder(self):
        exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
        cwd  = os.getcwd()
        print(f"Procurando imagens em: {cwd}")
        try:
            for f in sorted(os.listdir(cwd)):
                if os.path.splitext(f)[1].lower() in exts:
                    full = os.path.join(cwd, f)
                    self.selected_images.append({'path': full, 'name': f, 'copies': 1})
                    print(f"  ✓ {f}")
        except Exception as e:
            print(f"✗ Erro: {e}")
        self.update_images_list()
        self.update_preview()

    def load_single_image(self, image_path):
        if not os.path.exists(image_path):
            messagebox.showerror("Erro", f"Arquivo não encontrado:\n{image_path}")
            return
        exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
        if os.path.splitext(image_path)[1].lower() not in exts:
            messagebox.showerror("Erro",
                f"Formato não suportado:\n{image_path}\n\nFormatos: {', '.join(exts)}")
            return
        filename = os.path.basename(image_path)
        self.selected_images.append(
            {'path': os.path.abspath(image_path), 'name': filename, 'copies': 1})
        print(f"✓ Imagem carregada: {filename}")
        self.update_images_list()
        self.update_preview()

    # ── Lista ─────────────────────────────────────────────────────────────────
    def update_images_list(self):
        self.images_listbox.delete(0, tk.END)
        for img in self.selected_images:
            self.images_listbox.insert(tk.END, f"{img['name']} ({img['copies']}x)")

    def update_selected_copies(self):
        sel = self.images_listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma imagem")
            return
        try:
            n = int(self.copies_var.get())
            if n > 0:
                self.selected_images[sel[0]]['copies'] = n
                self.update_images_list()
                self.update_preview()
        except ValueError:
            messagebox.showerror("Erro", "Número de cópias inválido")

    def add_images(self):
        files = filedialog.askopenfilenames(
            title="Selecionar Imagens",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                       ("Todos", "*.*")])
        for f in files:
            if not any(img['path'] == f for img in self.selected_images):
                self.selected_images.append(
                    {'path': f, 'name': os.path.basename(f), 'copies': 1})
        self.update_images_list()
        self.update_preview()

    def remove_image(self):
        sel = self.images_listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma imagem")
            return
        del self.selected_images[sel[0]]
        self.update_images_list()
        self.update_preview()

    def clear_all(self):
        if messagebox.askyesno("Confirmar", "Remover todas as imagens?"):
            self.selected_images = []
            self.update_images_list()
            self.update_preview()

    # ── Preview ───────────────────────────────────────────────────────────────
    def update_preview(self):
        cv = self.preview_canvas
        cv.delete("all")
        cw = cv.winfo_width()
        ch = cv.winfo_height()

        # Aguarda a janela ter dimensões reais
        if cw < 10:
            self.root.after(80, self.update_preview)
            return

        if not self.selected_images:
            cv.create_rectangle(0, 0, cw, ch, fill=self.c('canvas_bg'), outline='')
            cv.create_text(cw / 2, ch / 2,
                           text="Nenhuma imagem selecionada",
                           font=("Arial", 12), fill=self.c('fg_secondary'))
            return

        cols, rows  = map(int, self.layout_var.get().split("x"))
        pw, ph      = self.paper_sizes[self.paper_var.get()]
        if self.orientation_var.get() == "Paisagem":
            pw, ph = ph, pw
        paper_ratio = pw / ph

        # Fundo do canvas
        cv.create_rectangle(0, 0, cw, ch, fill=self.c('canvas_bg'), outline='')

        # Dimensões do "papel" no canvas
        pad     = 20
        avail_w = cw - pad * 2
        avail_h = ch - pad * 2
        if avail_w / max(avail_h, 1) > paper_ratio:
            page_h = avail_h
            page_w = int(page_h * paper_ratio)
        else:
            page_w = avail_w
            page_h = int(page_w / paper_ratio)

        page_x = int((cw - page_w) / 2)
        page_y = int((ch - page_h) / 2)

        # Sombra
        shadow = "#555555" if self.current_theme == 'dark' else "#bbbbbb"
        cv.create_rectangle(page_x + 4, page_y + 4,
                            page_x + page_w + 4, page_y + page_h + 4,
                            fill=shadow, outline='')
        # Papel
        cv.create_rectangle(page_x, page_y, page_x + page_w, page_y + page_h,
                            fill=self.c('preview_paper'), outline=self.c('border'), width=1)
        # Rótulo
        cv.create_text(page_x + page_w / 2, page_y - 10,
                       text=f"{self.paper_var.get()} — {self.orientation_var.get()}",
                       font=("Arial", 9, "bold"), fill=self.c('preview_text'))

        # Células
        margin_px = int(int(self.margin_var.get()) / 210 * page_w)
        cell_w    = (page_w - margin_px * 2) / cols
        cell_h    = (page_h - margin_px * 2) / rows

        all_images = []
        for img_data in self.selected_images:
            for _ in range(img_data['copies']):
                all_images.append(img_data)

        ipp         = cols * rows
        total_pages = max(1, (len(all_images) + ipp - 1) // ipp)
        if self.current_page >= total_pages:
            self.current_page = 0

        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")

        start = self.current_page * ipp
        for pos, idx in enumerate(range(start, min(start + ipp, len(all_images)))):
            row = pos // cols
            col = pos % cols
            x   = int(page_x + margin_px + col * cell_w + 5)
            y   = int(page_y + margin_px + row * cell_h + 5)
            w   = int(cell_w - 10)
            h   = int(cell_h - 10)

            cv.create_rectangle(x, y, x + w, y + h,
                                outline=self.c('border'), width=1,
                                fill=self.c('preview_paper'))
            try:
                img = Image.open(all_images[idx]['path'])
                img.thumbnail((w - 10, h - 10), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.preview_images[idx] = photo  # mantém referência
                img_x = x + (w - photo.width()) // 2
                img_y = y + (h - photo.height()) // 2
                cv.create_image(img_x, img_y, image=photo, anchor=tk.NW)
                cv.create_text(x + 5, y + h - 12,
                               text=all_images[idx]['name'][:20],
                               font=("Arial", 7), anchor=tk.SW,
                               fill=self.c('fg_secondary'))
            except Exception as e:
                cv.create_text(x + w / 2, y + h / 2,
                               text=f"Erro: {str(e)[:30]}",
                               font=("Arial", 7), fill="red")

        total_copies = sum(img['copies'] for img in self.selected_images)
        self.info_label.config(
            text=f"Total: {len(self.selected_images)} imagem(ns) | "
                 f"{total_copies} cópia(s) | {total_pages} página(s)")

    def change_page(self, direction):
        cols, rows  = map(int, self.layout_var.get().split("x"))
        ipp         = cols * rows
        total       = sum(img['copies'] for img in self.selected_images)
        total_pages = max(1, (total + ipp - 1) // ipp)
        self.current_page = (self.current_page + direction) % total_pages
        self.update_preview()

    # ── PDF ───────────────────────────────────────────────────────────────────
    def _build_pdf(self, filename):
        if not REPORTLAB_AVAILABLE:
            raise Exception("reportlab não instalado — pip3 install reportlab")

        cols, rows = map(int, self.layout_var.get().split("x"))
        _sizes     = {"A4": A4, "A3": A3, "A5": A5, "Carta": letter}
        pagesize   = _sizes.get(self.paper_var.get(), A4)
        if self.orientation_var.get() == "Paisagem":
            pagesize = (pagesize[1], pagesize[0])

        margin = int(self.margin_var.get()) * mm
        c      = reportlab_canvas.Canvas(filename, pagesize=pagesize)
        pw, ph = pagesize
        cell_w = (pw - 2 * margin) / cols
        cell_h = (ph - 2 * margin) / rows

        all_images = []
        for img_data in self.selected_images:
            for _ in range(img_data['copies']):
                all_images.append(img_data['path'])

        ipp         = cols * rows
        total_pages = max(1, (len(all_images) + ipp - 1) // ipp)

        for page_num in range(total_pages):
            start = page_num * ipp
            for pos, abs_pos in enumerate(range(start, min(start + ipp, len(all_images)))):
                row  = pos // cols
                col  = pos % cols
                x    = margin + col * cell_w
                y    = ph - margin - (row + 1) * cell_h
                try:
                    img      = Image.open(all_images[abs_pos])
                    iw, ih   = cell_w - 10 * mm, cell_h - 10 * mm
                    w0, h0   = img.size
                    ratio    = min(iw / w0, ih / h0)
                    nw, nh   = int(w0 * ratio), int(h0 * ratio)
                    c.drawImage(all_images[abs_pos],
                                x + (cell_w - nw) / 2,
                                y + (cell_h - nh) / 2,
                                width=nw, height=nh)
                except Exception as e:
                    c.drawString(x + 10, y + 10, f"Erro: {str(e)[:30]}")
            if page_num < total_pages - 1:
                c.showPage()

        c.save()

    def generate_pdf(self):
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Erro", "reportlab não instalado.\npip3 install reportlab")
            return
        if not self.selected_images:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf"), ("Todos", "*.*")],
            initialfile="impressao.pdf")
        if not filename:
            return
        try:
            self._build_pdf(filename)
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\n{filename}")
            os.system(f'xdg-open "{filename}" 2>/dev/null &')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF:\n{e}")
            traceback.print_exc()

    # ── Impressão ─────────────────────────────────────────────────────────────
    def print_action(self):
        if not self.selected_images:
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada")
            return

        printer = self.printer_var.get()

        if printer in ("Nenhuma impressora", "Simular (PDF)"):
            messagebox.showinfo("Simulação",
                "Nenhuma impressora CUPS encontrada.\n"
                "Gerando PDF para visualização...")
            self.generate_pdf()
            return

        if not CUPS_AVAILABLE or not self.cups_conn:
            messagebox.showerror("Erro",
                "CUPS não está disponível.\n"
                "Instale com: sudo apt-get install python3-cups")
            return

        try:
            import tempfile, atexit
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp_path = tmp.name

            self._build_pdf(tmp_path)

            job_id = self.cups_conn.printFile(
                printer, tmp_path, "Impressão de Imagens",
                {"media":         self.paper_var.get(),
                 "print-quality": self.quality_var.get()})

            messagebox.showinfo("Sucesso",
                f"✓ Impressão enviada!\nImpressora: {printer}\nJob ID: {job_id}")
            atexit.register(
                lambda: os.unlink(tmp_path) if os.path.exists(tmp_path) else None)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir:\n{e}")
            traceback.print_exc()


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    """
    Uso:
        python3 print_images.py              # escaneia pasta atual
        python3 print_images.py imagem.jpg   # abre uma imagem específica
    """
    root = tk.Tk()
    ImagePrintDialog(root, image_path=sys.argv[1] if len(sys.argv) > 1 else None)
    root.mainloop()


if __name__ == "__main__":
    main()
