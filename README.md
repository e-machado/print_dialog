# Print Dialog - Simulador de Interface de Impressão

Um programa Linux que recria a interface de impressão mostrada na imagem, permitindo simular e testar fluxos de impressão de imagens.

## 📋 Requisitos

### Mínimo (tkinter)
- Python 3.6+
- tkinter (geralmente incluído com Python)

### Recomendado (com preview de imagens)
- Python 3.6+
- tkinter
- Pillow (PIL)

## 🚀 Instalação

### 1. Versão com tkinter (Simples)

**Debian/Ubuntu:**
```bash
sudo apt-get install python3 python3-tk python3-pip
pip3 install Pillow
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-tkinter python3-pip
pip3 install Pillow
```

**Arch:**
```bash
sudo pacman -S python tk python-pip
pip install Pillow
```

### 2. Versão com PyQt5 (Profissional)

**Debian/Ubuntu:**
```bash
sudo apt-get install python3 python3-pyqt5 python3-pip
pip3 install Pillow
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-devel python3-pip qt5-qtbase
pip3 install PyQt5 Pillow
```

## 📝 Uso

### Versão tkinter:
```bash
python3 print_dialog.py
```

Ou torne executável:
```bash
chmod +x print_dialog.py
./print_dialog.py
```

### Versão PyQt5 (mais profissional):
```bash
python3 print_dialog_pyqt5.py
```

## 🎯 Funcionalidades

✅ Seleção de impressora
✅ Tamanho do papel (A3, A4, A5, Ofício, Carta)
✅ Qualidade de impressão (Rascunho, Normal, Alta, Máxima)
✅ Tipo de papel (Comum, Fotográfico, Espesso)
✅ Gerenciamento de cópias
✅ Opções de ajuste de imagem
✅ Preview de imagens
✅ Lista de imagens selecionadas
✅ Navegação de páginas

## 🔧 Personalizações

Você pode modificar o programa para:

1. **Integrar com CUPS (Common Unix Printing System)**
   ```python
   import cups
   conn = cups.Connection()
   printers = conn.getPrinters()
   ```

2. **Adicionar suporte a impressão real**
   ```python
   from subprocess import run
   run(['lp', '-d', printer_name, image_file])
   ```

3. **Adicionar preview de imagens reais**
   ```python
   from PIL import Image
   img = Image.open(file_path)
   # Renderizar na canvas
   ```

4. **Salvar configurações**
   ```python
   import json
   with open('print_config.json', 'w') as f:
       json.dump(config, f)
   ```

## 📂 Estrutura do Código

```
PrintDialog (classe principal)
├── setup_ui() - Configura toda a interface
├── create_options_section() - Opções de impressora
├── create_preview_section() - Preview das imagens
├── create_additional_options() - Lista de imagens
├── create_bottom_controls() - Controles de cópias
├── create_buttons() - Botões de ação
└── print_action() - Ação de impressão
```

## 🎨 Customizações Visuais

Para mudar cores:
```python
header = tk.Frame(self.root, bg="#0066CC")  # Azul
close_btn = tk.Button(..., bg="#CC0000")    # Vermelho
```

Para mudar fontes:
```python
title = tk.Label(..., font=("Arial", 12, "bold"))
```

## 🐛 Troubleshooting

### Erro: "No module named 'tkinter'"
```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (se necessário)
brew install python-tk
```

### Erro: "No module named 'PIL'"
```bash
pip3 install Pillow
```

### Interface lenta
- Reduza o tamanho das imagens de preview
- Use versão PyQt5 para melhor performance
- Considere usar PySimpleGUI para algo mais leve

## 📚 Versões Alternativas Disponíveis

1. **print_dialog.py** - tkinter (leve, sem dependências)
2. **print_dialog_pyqt5.py** - PyQt5 (profissional, nativo)
3. **print_dialog_web.py** - Flask + HTML/CSS (web-based)

## 💡 Próximos Passos

Para integração real com impressoras:

```python
# 1. Instale cups-python
pip3 install pycups

# 2. Obtenha lista de impressoras
import cups
conn = cups.Connection()
printers = conn.getPrinters()

# 3. Envie trabalho de impressão
conn.printFile(printer_name, filename, "Print Job", {})
```

## 📄 Licença

Código livre para uso educacional e comercial.

## 👨‍💻 Autor

Criado como simulador de interface de impressão do CUPS para Linux.
