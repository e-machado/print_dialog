# 🖨️ Sistema de Impressão de Imagens - Guia Completo

## O que é?

Um programa **Linux funcional** que permite:
- ✅ Carregar automaticamente imagens da pasta atual
- ✅ Visualizar layout real de impressão antes de enviar
- ✅ Configurar disposição de imagens (1x1, 2x1, 2x2, 3x3)
- ✅ Repetir imagens de acordo com número de cópias
- ✅ Gerar PDF com o layout final
- ✅ Imprimir diretamente na impressora CUPS do sistema

---

## 📥 Instalação Rápida

### 1️⃣ Um Comando (Recomendado)
```bash
chmod +x install_print.sh
./install_print.sh
```

### 2️⃣ Manual (Debian/Ubuntu)
```bash
# Atualizar
sudo apt-get update

# Instalar dependências essenciais
sudo apt-get install -y python3 python3-tk python3-dev python3-pip

# Instalar CUPS (sistema de impressão)
sudo apt-get install -y cups python3-cups

# Instalar bibliotecas Python
pip3 install --user Pillow reportlab pycups
```

### 3️⃣ Manual (Fedora/RHEL)
```bash
sudo dnf install -y python3 python3-tkinter python3-devel python3-pip
sudo dnf install -y cups python3-cups
pip3 install --user Pillow reportlab pycups
```

### 4️⃣ Manual (Arch)
```bash
sudo pacman -S python tk python-pip
sudo pacman -S cups
pip install --user Pillow reportlab
```

---

## 🚀 Como Usar

### Passo 1: Prepare as Imagens
```bash
# Copie suas imagens para a pasta do programa
cd ~/Documentos/impressao
cp ~/Downloads/*.jpg .
```

### Passo 2: Execute o Programa
```bash
python3 print_images_real.py
```

ou

```bash
./print_images_real.py
```

### Passo 3: Configure a Impressão

**A. Carregamento Automático**
- Imagens da pasta atual aparecem na lista automaticamente
- Total de imagens e cópias mostrado na interface

**B. Escolha a Impressora**
- Selecione sua impressora na dropdown
- Se nenhuma aparecer, use "Simular (PDF)"

**C. Configure o Papel**
- A4 (padrão)
- A3 (maior)
- A5 (menor)
- Carta

**D. Escolha a Disposição**
- **1x1**: Uma imagem por página
- **2x1**: Duas imagens lado a lado
- **2x2**: Quatro imagens (2x2)
- **3x3**: Nove imagens (3x3)

**E. Configure as Cópias**
1. Selecione imagem na lista
2. Digite número de cópias
3. Clique "Atualizar"

### Passo 4: Visualize
Clique **"Visualizar PDF"** para ver exatamente como ficará

### Passo 5: Imprima
Clique **"Imprimir"** para enviar para impressora

---

## 📋 Interface Explicada

```
┌─────────────────────────────────────────────────┐
│ Imprimir Imagens - Sistema Real de Impressão   │
├──────────────┬──────────────────────────────────┤
│  OPÇÕES      │  PREVIEW                         │
│              │                                  │
│ Impressora   │  ┌──┬──┐                         │
│ [dropdown]   │  │░░│░░│  Página 1 de 2         │
│              │  ├──┼──┤                         │
│ Papel: A4    │  │░░│░░│  ◀  ▶                  │
│ [dropdown]   │  └──┴──┘                         │
│              │                                  │
│ Qualidade    │  Total: 4 imagens | 8 cópias   │
│ [dropdown]   │  4 páginas                      │
│              │                                  │
│ Disposição   │                                  │
│ 2x2 [v]      │                                  │
│              │                                  │
│ Margem: 10mm │                                  │
│              │                                  │
│ ──────────── │                                  │
│ Imagens      │                                  │
│              │                                  │
│ [X] img1.jpg │                                  │
│ [X] img2.png │                                  │
│ [ ] img3.jpg │                                  │
│              │                                  │
│ Cópias: [2]  │                                  │
│ [ Atualizar] │                                  │
│              │                                  │
│ [Adicionar]  │                                  │
│ [Remover]    │                                  │
│ [Limpar]     │                                  │
└──────────────┴──────────────────────────────────┘
[Visualizar PDF] ────────────────────────────────
                    [Cancelar] [Imprimir]
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Imprimir 8 fotos 10x15 em A4

1. **Prepare**: Coloque 8 imagens na pasta
2. **Disposição**: Selecione "2x2" (4 fotos por página)
3. **Cópias**: Deixe todas com 1 cópia
4. **Resultado**: 2 páginas com 4 fotos cada

### Exemplo 2: Imprimir 1 foto em 3 cópias

1. **Carregue**: 1 imagem na lista
2. **Cópias**: Selecione a imagem, defina 3 cópias
3. **Disposição**: Mantenha "1x1"
4. **Resultado**: 3 páginas, cada uma com a mesma foto

### Exemplo 3: Impressão Profissional

1. **Imagens**: 4 fotos de produtos
2. **Disposição**: "2x2" (4 produtos por página)
3. **Cópias**: 10 cópias de cada produto
4. **Resultado**: 40 páginas totais

---

## 🎨 Personalizações

### Mudar Margem
```
Margem: [10] mm
```
- Mínimo: 0 mm
- Máximo: 50 mm
- Padrão: 10 mm

### Ajustar Qualidade
```
Qualidade: [Normal ▼]
```
- Rascunho: Mais rápido
- Normal: Qualidade padrão
- Alta: Melhor qualidade

---

## 🔧 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'cups'"

```bash
# Opção 1: Debian/Ubuntu
sudo apt-get install python3-cups

# Opção 2: Via pip
pip3 install pycups

# Opção 3: Usar em modo simulação
# O programa funciona sem CUPS, gerando PDFs
```

### ❌ "No module named 'PIL'"

```bash
pip3 install --user Pillow
```

### ❌ "No module named 'reportlab'"

```bash
pip3 install --user reportlab
```

### ❌ Nenhuma impressora aparece

**Causas comuns:**
1. CUPS não está instalado
2. CUPS não está rodando
3. Impressora não está ligada/conectada

**Soluções:**

```bash
# Verificar se CUPS está rodando
sudo systemctl status cups

# Iniciar CUPS
sudo systemctl start cups

# Habilitar CUPS no boot
sudo systemctl enable cups

# Ver impressoras disponíveis
lpstat -p -d

# Testar com impressora virtual
sudo lpadmin -p PDF -E -v file:///dev/null -m drv:///sample.drv/generic.ppd
```

### ❌ Imagens aparecem cortadas/distorcidas

**Solução:**
- Aumente a margem
- Use disposição menor (1x1 ou 2x1)
- Reduza tamanho das imagens originais

---

## 📊 Especificações Técnicas

### Formatos Suportados
- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)
- WebP (.webp)

### Tamanhos de Papel
| Nome | Dimensões | Uso |
|------|-----------|-----|
| A4 | 210 × 297 mm | Padrão |
| A3 | 297 × 420 mm | Pôster |
| A5 | 148 × 210 mm | Pequeno |
| Carta | 216 × 279 mm | EUA |

### Disposições
| Layout | Imagens/Página | Páginas (8 fotos) |
|--------|---|---|
| 1×1 | 1 | 8 |
| 2×1 | 2 | 4 |
| 2×2 | 4 | 2 |
| 3×3 | 9 | 1 |

---

## 🎯 Dicas Profissionais

### 1. Preparar Imagens
```bash
# Converter para dimensões padrão
for img in *.jpg; do
  convert "$img" -resize 1920x1080 "resized_$img"
done
```

### 2. Batch Printing
```bash
# Copiar mesma imagem 10 vezes
for i in {1..10}; do
  cp original.jpg "copia_$i.jpg"
done

# Abrir com 10 cópias automáticas
```

### 3. Otimizar para Web
```bash
# Reduzir tamanho mantendo qualidade
for img in *.jpg; do
  convert "$img" -quality 85 -resize 2000x2000 "opt_$img"
done
```

---

## 📄 Saída em PDF

O programa gera PDFs com:
- ✅ Layout exato de impressão
- ✅ Margens configuráveis
- ✅ Disposição preservada
- ✅ Pronto para copiadoras

Visualizar antes de imprimir economiza papel! 📄

---

## 🐛 Log de Erros

O programa mostra mensagens úteis:

```
✓ CUPS conectado. Impressoras: ['HP-Laserjet', 'Canon-Pixma']
✓ Encontrada: foto1.jpg
✓ Encontrada: foto2.png
✗ Erro ao carregar: corrupted.jpg
```

---

## 🔐 Permissões

Se tiver problemas de permissão:

```bash
# Adicionar ao grupo de impressoras
sudo usermod -aG lpadmin $USER

# Aplicar permissões
newgrp lpadmin

# Logout e login
exit
```

---

## 📞 Suporte

### Testar Instalação
```bash
./install_print.sh
# Selecione opção para verificar
```

### Diagnóstico Completo
```bash
echo "Python:"
python3 --version

echo "Tkinter:"
python3 -c "import tkinter; print('OK')"

echo "PIL:"
python3 -c "import PIL; print('OK')"

echo "reportlab:"
python3 -c "import reportlab; print('OK')"

echo "CUPS:"
lpstat -p -d
```

---

## 🎓 Aprender Mais

- [CUPS Documentation](https://www.cups.org/)
- [PIL/Pillow Docs](https://pillow.readthedocs.io/)
- [ReportLab Guide](https://www.reportlab.com/)
- [Python tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)

---

## ✅ Checklist Antes de Imprimir

- [ ] Imagens carregadas (lista não vazia)
- [ ] Impressora selecionada
- [ ] Número de cópias correto
- [ ] Papel correto na impressora
- [ ] Toner/tinta verificado
- [ ] Visualização PDF conferida
- [ ] Margens adequadas

---

## 🎉 Pronto!

Você tem um sistema completo de impressão de imagens funcional no Linux!

```bash
python3 print_images_real.py
```

Aproveite! 📸🖨️
