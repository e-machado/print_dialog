#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print Dialog (PyQt5 Version)
Versão profissional com PyQt5 - mais semelhante à interface original
"""

import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QPushButton, QSpinBox, 
                             QCheckBox, QListWidget, QListWidgetItem, QScrollArea,
                             QFrame, QSplitter, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QPixmap, QIcon

class PrintDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Imprimir Imagens")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Conteúdo principal
        content = self.create_content()
        main_layout.addWidget(content)
        
        # Rodapé com botões
        footer = self.create_footer()
        main_layout.addLayout(footer)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Cria o header azul com título"""
        header = QFrame()
        header.setStyleSheet("background-color: #0066CC;")
        header.setFixedHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        
        title = QLabel("📄 Imprimir Imagens")
        title.setFont(QFont("Arial", 11, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #CC0000;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #990000;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        header.setLayout(layout)
        return header
    
    def create_content(self):
        """Cria o conteúdo principal"""
        content = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Pergunta
        question = QLabel("Como deseja imprimir as imagens?")
        question.setFont(QFont("Arial", 10))
        layout.addWidget(question)
        
        # Opções de impressão
        options_layout = self.create_options()
        layout.addLayout(options_layout)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Conteúdo principal (preview + lista)
        main_content = self.create_main_content()
        layout.addWidget(main_content)
        
        content.setLayout(layout)
        return content
    
    def create_options(self):
        """Cria as opções de impressão"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        options = [
            ("Impressora:", ["MONTY-SCTI - HP LaserJet MFI", "Printer 2", "Printer 3"]),
            ("Tamanho do papel:", ["A3", "A4", "A5", "Ofício", "Carta"]),
            ("Qualidade:", ["Rascunho", "Normal", "Alta", "Máxima"]),
            ("Tipo de papel:", ["Padrão da impressora", "Comum", "Fotográfico", "Espesso"]),
        ]
        
        for label_text, values in options:
            label = QLabel(label_text)
            label.setFixedWidth(130)
            label.setFont(QFont("Arial", 9))
            
            combo = QComboBox()
            combo.addItems(values)
            combo.setFixedHeight(25)
            
            layout.addWidget(label)
            layout.addWidget(combo)
        
        return layout
    
    def create_main_content(self):
        """Cria a área de conteúdo principal com preview e lista"""
        splitter = QSplitter(Qt.Horizontal)
        
        # Preview área
        preview_frame = self.create_preview()
        splitter.addWidget(preview_frame)
        
        # Lista de imagens
        list_frame = self.create_image_list()
        splitter.addWidget(list_frame)
        
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        return splitter
    
    def create_preview(self):
        """Cria a área de preview"""
        frame = QFrame()
        frame.setStyleSheet("border: 1px solid #CCCCCC;")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Canvas de preview
        preview_label = QLabel()
        preview_label.setMinimumHeight(350)
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet("background-color: #F5F5F5; border: 2px dashed #999;")
        preview_label.setText("Preview das imagens\n(Selecione imagens para visualizar)")
        preview_label.setFont(QFont("Arial", 11))
        preview_label.setStyleSheet("""
            QLabel {
                background-color: #F5F5F5;
                border: 2px dashed #999;
                color: #666;
            }
        """)
        layout.addWidget(preview_label)
        
        # Navegação
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        nav_label = QLabel("1 de 1 página")
        nav_label.setFont(QFont("Arial", 9))
        nav_layout.addWidget(nav_label)
        
        nav_layout.addStretch()
        
        prev_btn = QPushButton("◀")
        prev_btn.setFixedWidth(30)
        nav_layout.addWidget(prev_btn)
        
        next_btn = QPushButton("▶")
        next_btn.setFixedWidth(30)
        nav_layout.addWidget(next_btn)
        
        layout.addLayout(nav_layout)
        
        frame.setLayout(layout)
        return frame
    
    def create_image_list(self):
        """Cria a lista de imagens"""
        frame = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        title = QLabel("Imagens selecionadas")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(title)
        
        # Lista de imagens
        self.image_list = QListWidget()
        self.image_list.setMinimumWidth(250)
        
        items = [
            "Foto de página inteira",
            "13 x 18 cm. (2)",
            "20 x 25 cm. (1)"
        ]
        
        for item in items:
            self.image_list.addItem(item)
        
        layout.addWidget(self.image_list)
        
        # Botões de controle
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        add_btn = QPushButton("Adicionar...")
        add_btn.setFixedHeight(28)
        add_btn.clicked.connect(self.add_image)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remover")
        remove_btn.setFixedHeight(28)
        remove_btn.clicked.connect(self.remove_image)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        
        frame.setLayout(layout)
        return frame
    
    def create_footer(self):
        """Cria o rodapé com controles e botões"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Cópias
        copies_label = QLabel("Cópias de cada imagem:")
        copies_label.setFont(QFont("Arial", 9))
        layout.addWidget(copies_label)
        
        copies_spin = QSpinBox()
        copies_spin.setValue(4)
        copies_spin.setRange(1, 10)
        copies_spin.setFixedWidth(50)
        layout.addWidget(copies_spin)
        
        # Checkbox
        self.adjust_check = QCheckBox("Ajustar imagem ao quadro")
        self.adjust_check.setFont(QFont("Arial", 9))
        layout.addWidget(self.adjust_check)
        
        layout.addStretch()
        
        # Botões de ação
        options_btn = QPushButton("Opções...")
        options_btn.setFixedWidth(100)
        layout.addWidget(options_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.close)
        layout.addWidget(cancel_btn)
        
        print_btn = QPushButton("Imprimir")
        print_btn.setFixedWidth(100)
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066CC;
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0052A3;
            }
        """)
        print_btn.clicked.connect(self.print_action)
        layout.addWidget(print_btn)
        
        return layout
    
    def add_image(self):
        """Adiciona imagem à lista"""
        file_dialog = QFileDialog()
        files, _ = file_dialog.getOpenFileNames(
            self,
            "Selecionar Imagens",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif);;Todos os Arquivos (*)"
        )
        
        for file in files:
            self.image_list.addItem(file.split('/')[-1])
    
    def remove_image(self):
        """Remove imagem selecionada"""
        current_row = self.image_list.currentRow()
        if current_row >= 0:
            self.image_list.takeItem(current_row)
    
    def print_action(self):
        """Ação de impressão"""
        message = """
✓ Configuração de Impressão:
═══════════════════════════════════════

Impressora: MONTY-SCTI - HP LaserJet MFI
Tamanho do papel: A4
Qualidade: Normal
Tipo de papel: Padrão da impressora
Cópias por imagem: 4
Ajustar ao quadro: Sim

Imagens selecionadas: 3

═══════════════════════════════════════
Impressão iniciada!
        """
        QMessageBox.information(self, "Imprimindo", message)
    
    def get_stylesheet(self):
        """Retorna o stylesheet da aplicação"""
        return """
        QDialog {
            background-color: #FFFFFF;
        }
        QLabel {
            color: #333333;
        }
        QComboBox {
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            padding: 5px;
            background-color: white;
        }
        QComboBox:hover {
            border: 1px solid #0066CC;
        }
        QPushButton {
            background-color: #F0F0F0;
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            padding: 5px 15px;
            font-size: 9pt;
        }
        QPushButton:hover {
            background-color: #E8E8E8;
        }
        QPushButton:pressed {
            background-color: #D0D0D0;
        }
        QSpinBox {
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            padding: 3px;
        }
        QListWidget {
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            background-color: white;
        }
        """

def main():
    app = QApplication(sys.argv)
    dialog = PrintDialog()
    dialog.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
