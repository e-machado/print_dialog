# 🖨️ Sistema de Impressão de Imagens para Linux

Um programa **100% funcional** que permite imprimir imagens com layout configurável, usando CUPS (sistema de impressão do Linux).

## ⚡ Início Rápido (3 passos)

### 1. Instalar Dependências
```bash
chmod +x install_print.sh
./install_print.sh
```

### 2. Criar Imagens de Teste (Opcional)
```bash
python3 criar_imagens_teste.py
cd test_images
```

### 3. Executar o Programa
```bash
python3 print_images_real.py
```

Pronto! A interface abre automaticamente.

---

## 📁 Arquivos Fornecidos

### Programas Principais
- **`print_images_real.py`** ⭐ - Programa funcional principal
  - Carrega impressoras CUPS reais
  - Carrega imagens da pasta atual
  - Preview em tempo real
  - Gera PDF
  - Envia para impressora

### Instalação e Configuração
- **`install_print.sh`** - Script automático de instalação
- **`criar_imagens_teste.py`** - Cria imagens coloridas para testar

### Documentação
- **`GUIA_COMPLETO.md`** - Guia detalhado com exemplos e troubleshooting
- **`README.md`** - Este arquivo

---

## 🎯 Funcionalidades

✅ **Carregamento Automático**
- Detecta todas as imagens da pasta atual
- Formatos: PNG, JPG, BMP, GIF, TIFF, WebP

✅ **Impressoras CUPS**
- Lista todas as impressoras do sistema
- Integração nativa com CUPS

✅ **Layout Flexível**
- 1×1: Uma imagem por página
- 2×1: Duas imagens lado a lado  
- 2×2: Quatro imagens (2×2)
- 3×3: Nove imagens (3×3)

✅ **Múltiplas Cópias**
- Configure cópias por imagem
- Sistema calcula páginas automaticamente

✅ **Visualização PDF**
- Veja exatamente como ficará antes de imprimir
- Salve como PDF para uso posterior

✅ **Impressão Real**
- Envie diretamente para qualquer impressora CUPS
- Suporte a diferentes tamanhos de papel
- Configuração de qualidade

---

## 🖥️ Requisitos do Sistema

### Mínimo
- Linux (qualquer distribuição)
- Python 3.6+
- 50 MB de espaço livre

### Recomendado
- Python 3.8+
- CUPS instalado e configurado
- Impressora conectada

---

## 📋 Instalação Detalhada

### Opção 1: Automática (Recomendada)
```bash
chmod +x install_print.sh
./install_print.sh
```

Detecta sua distribuição e instala tudo automaticamente.

### Opção 2: Manual - Debian/Ubuntu
```bash
# Atualizar repositórios
sudo apt-get update

# Instalar Python e tkinter
sudo apt-get install -y python3 python3-tk python3-dev python3-pip

# Instalar CUPS (sistema de impressão)
sudo apt-get install -y cups python3-cups

# Instalar bibliotecas Python
pip3 install --user Pillow reportlab pycups

# Adicionar ao grupo de impressoras
sudo usermod -aG lpadmin $USER
```

### Opção 3: Manual - Fedora/RHEL
```bash
sudo dnf install -y python3 python3-tkinter python3-devel python3-pip
sudo dnf install -y cups python3-cups
pip3 install --user Pillow reportlab pycups
sudo usermod -aG lpadmin $USER
```

### Opção 4: Manual - Arch
```bash
sudo pacman -S --noconfirm python tk python-pip cups
pip install --user Pillow reportlab
sudo usermod -aG lpadmin $USER
```

---

## 🚀 Primeira Execução

### 1. Prepare as Imagens
```bash
# Opção A: Use imagens de teste
python3 criar_imagens_teste.py
cd test_images

# Opção B: Copie suas próprias imagens
cp ~/Downloads/*.jpg .
```

### 2. Execute o Programa
```bash
python3 print_images_real.py
```

### 3. Configure na Interface
1. Imagens aparecem automaticamente na lista
2. Selecione a disposição desejada (ex: 2×2)
3. Ajuste número de cópias
4. Clique "Visualizar PDF"

### 4. Imprima
- Se tiver impressora: Clique "Imprimir"
- Se não: Use "Simular (PDF)" para gerar arquivo

---

## 🎮 Como Usar

### Layout Básico

```
┌─ OPÇÕES ESQUERDA ──┬─────────────────────────┐
│                    │                         │
│ Impressora: [v]    │  ╔═══════════════════╗  │
│ Papel: A4          │  ║ PREVIEW EM TEMPO  ║  │
│ Qualidade: Normal  │  ║ REAL DA IMPRESSÃO ║  │
│ Disposição: 2x2    │  ║                   ║  │
│ Margem: 10mm       │  ║   [IMG] [IMG]    ║  │
│ ──────────────     │  ║   [IMG] [IMG]    ║  │
│ Imagens:           │  ║                   ║  │
│ [✓] foto1.jpg      │  ╚═══════════════════╝  │
│ [✓] foto2.png      │  Pág 1/2                │
│ [ ] foto3.jpg      │  ◀    ▶                 │
│                    │                         │
│ Cópias: [3]        │ Total: 3 imagens        │
│ [Atualizar]        │ 7 cópias | 2 páginas   │
│ [Adicionar]        │                         │
│ [Remover]          │                         │
│ [Limpar]           │                         │
└────────────────────┴─────────────────────────┘
[Visualizar PDF] ────────────────────────────────
                    [Cancelar]  [Imprimir]
```

### Fluxo de Trabalho

```
1. Imagens Carregadas
   ↓
2. Selecione Disposição (1×1, 2×1, 2×2, 3×3)
   ↓
3. Configure Cópias
   ↓
4. Visualize PDF
   ↓
5. Imprima
```

---

## 💾 Exemplos Prácticos

### Exemplo 1: Fotos 10×15 em A4

```
Imagens: 8 fotos
Disposição: 2×2 (4 por página)
Cópias: 1 cada
Resultado: 2 páginas
```

### Exemplo 2: Mesmo Documento 10 Vezes

```
Imagens: 1 documento
Cópias: 10
Disposição: 1×1
Resultado: 10 páginas
```

### Exemplo 3: Catálogo Profissional

```
Imagens: 10 produtos
Disposição: 2×2
Cópias: 5 cada
Resultado: 13 páginas
```

---

## 🔧 Verificar Instalação

Execute este script para verificar tudo:

```bash
echo "=== Verificação de Instalação ==="
echo ""
echo "Python:"
python3 --version

echo ""
echo "Tkinter:"
python3 -c "import tkinter; print('✓ OK')" || echo "✗ Não instalado"

echo ""
echo "Pillow:"
python3 -c "import PIL; print('✓ OK')" || echo "✗ Não instalado"

echo ""
echo "reportlab:"
python3 -c "import reportlab; print('✓ OK')" || echo "✗ Não instalado"

echo ""
echo "CUPS:"
python3 -c "import cups; print('✓ OK')" || echo "⚠ Não instalado (modo simulação)"

echo ""
echo "Impressoras:"
lpstat -p -d || echo "⚠ CUPS não rodando"
```

---

## 🐛 Resolver Problemas

### Nenhuma imagem aparece

**Verificar:**
```bash
# Ver imagens na pasta
ls -la *.{jpg,png,jpeg,bmp,gif,tiff,webp} 2>/dev/null

# Se nada aparecer, criar imagens de teste
python3 criar_imagens_teste.py
```

### Nenhuma impressora aparece

**Solução 1 - Reiniciar CUPS:**
```bash
sudo systemctl restart cups
```

**Solução 2 - Verificar impressoras:**
```bash
lpstat -p -d
```

**Solução 3 - Usar modo simulação:**
- Selecione "Simular (PDF)"
- Gere PDF em vez de imprimir

### Erro "ModuleNotFoundError: No module named 'PIL'"

```bash
pip3 install --user Pillow
```

### Erro "ModuleNotFoundError: No module named 'reportlab'"

```bash
pip3 install --user reportlab
```

### Erro "ModuleNotFoundError: No module named 'cups'"

```bash
# Opção 1: Debian/Ubuntu
sudo apt-get install python3-cups

# Opção 2: Via pip
pip3 install --user pycups

# Opção 3: Usar sem CUPS (modo simulação)
```

### Interface lenta

**Soluções:**
1. Reduza tamanho das imagens
2. Use menos imagens por página
3. Feche outros programas

---

## 📊 Especificações

### Formatos Suportados
- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)
- WebP (.webp)

### Tamanhos de Papel
- **A4** (210 × 297 mm) - Padrão
- **A3** (297 × 420 mm) - Grande
- **A5** (148 × 210 mm) - Pequeno
- **Carta** (216 × 279 mm) - EUA

### Disposições Disponíveis
- **1×1**: 1 imagem/página (normal)
- **2×1**: 2 imagens lado a lado
- **2×2**: 4 imagens em grade
- **3×3**: 9 imagens em grade

---

## 🎓 Documentação Completa

Para mais informações e exemplos avançados, veja:

📖 **`GUIA_COMPLETO.md`** - Guia detalhado com:
- Todas as funcionalidades
- Exemplos práticos
- Dicas profissionais
- Troubleshooting avançado
- Recursos adicionais

---

## 📞 Suporte Rápido

### Teste a Instalação
```bash
python3 -c "
import tkinter
from PIL import Image
from reportlab.lib.pagesizes import A4
print('✓ Todas as dependências OK!')
"
```

### Teste o Programa
```bash
# Com imagens de teste
python3 criar_imagens_teste.py
cd test_images
python3 ../print_images_real.py
```

### Ver Log de Execução
```bash
python3 print_images_real.py 2>&1 | tee output.log
```

---

## ✅ Checklist

Antes de imprimir, verifique:

- [ ] Imagens carregadas (lista não vazia)
- [ ] Impressora selecionada e disponível
- [ ] Papel correto na impressora
- [ ] Toner/tinta verificado
- [ ] Cópias configuradas corretamente
- [ ] Preview PDF conferido
- [ ] Margens adequadas

---

## 🎉 Começar Agora

```bash
# 1. Instalar
./install_print.sh

# 2. Criar imagens de teste (opcional)
python3 criar_imagens_teste.py
cd test_images

# 3. Executar
python3 ../print_images_real.py
```

Aproveite seu sistema de impressão 100% funcional! 📸🖨️

---

## 📄 Licença

Código livre para uso educacional e comercial.

---

## 🤝 Contribuições

Se encontrar problemas ou tiver sugestões, sinta-se à vontade para:
1. Testar em diferentes ambientes
2. Reportar bugs
3. Sugerir melhorias

---

**Versão:** 1.0  
**Data:** 2026  
**Sistema:** Linux (todas as distribuições)
