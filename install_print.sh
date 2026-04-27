#!/bin/bash

# Script de instalação para print_images_real.py

echo "╔════════════════════════════════════════════════╗"
echo "║  Sistema de Impressão de Imagens - Instalação  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Detectar distribuição
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO="$ID"
fi

echo "🔍 Sistema detectado: $DISTRO"
echo ""

# Instalação de dependências
echo "📦 Instalando dependências..."

case "$DISTRO" in
    ubuntu|debian)
        echo "   → Atualizando pacotes..."
        sudo apt-get update -qq
        
        echo "   → Instalando Python3 e tkinter..."
        sudo apt-get install -y python3 python3-tk python3-dev python3-pip >/dev/null 2>&1
        
        echo "   → Instalando CUPS (impressoras)..."
        sudo apt-get install -y cups python3-cups >/dev/null 2>&1
        
        echo "   → Adicionando usuário ao grupo lpadmin..."
        sudo usermod -aG lpadmin $USER 2>/dev/null || true
        ;;
    fedora|rhel|centos)
        echo "   → Instalando Python3 e tkinter..."
        sudo dnf install -y python3 python3-tkinter python3-devel python3-pip >/dev/null 2>&1
        
        echo "   → Instalando CUPS..."
        sudo dnf install -y cups python3-cups >/dev/null 2>&1
        ;;
    arch)
        echo "   → Instalando Python3 e tkinter..."
        sudo pacman -S --noconfirm python tk python-pip >/dev/null 2>&1
        
        echo "   → Instalando CUPS..."
        sudo pacman -S --noconfirm cups python-pycups >/dev/null 2>&1
        ;;
    *)
        echo "   ⚠ Distribuição não reconhecida"
        echo "   Instale manualmente: python3, python3-tk, python3-dev, cups"
        ;;
esac

echo ""
echo "📚 Instalando bibliotecas Python..."

echo "   → Pillow (manipulação de imagens)..."
pip3 install --user Pillow >/dev/null 2>&1

echo "   → reportlab (geração de PDF)..."
pip3 install --user reportlab >/dev/null 2>&1

echo "   → pycups (integração CUPS)..."
pip3 install --user pycups >/dev/null 2>&1 || sudo apt-get install -y python3-cups >/dev/null 2>&1

echo ""
echo "✅ Dependências instaladas!"

# Tornar executável
echo ""
echo "🔧 Configurando arquivo..."
chmod +x print_images_real.py

echo "✓ Arquivo print_images_real.py é executável"
echo ""

# Verificar instalação
echo "🔍 Verificando instalação..."
echo ""

python3 -c "import tkinter; print('  ✓ tkinter OK')" 2>/dev/null || echo "  ✗ tkinter com problema"
python3 -c "import PIL; print('  ✓ Pillow OK')" 2>/dev/null || echo "  ✗ Pillow não instalado"
python3 -c "import reportlab; print('  ✓ reportlab OK')" 2>/dev/null || echo "  ✗ reportlab não instalado"
python3 -c "import cups; print('  ✓ CUPS/pycups OK')" 2>/dev/null || echo "  ✗ CUPS/pycups não instalado"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 COMO USAR:"
echo ""
echo "1. Coloque suas imagens na pasta atual:"
echo "   cp /caminho/para/imagens/*.jpg ."
echo ""
echo "2. Execute o programa:"
echo "   python3 print_images_real.py"
echo "   ou"
echo "   ./print_images_real.py"
echo ""
echo "3. Use a interface para:"
echo "   • Selecionar disposição (1x1, 2x1, 2x2, 3x3)"
echo "   • Definir número de cópias"
echo "   • Visualizar PDF antes de imprimir"
echo "   • Enviar para impressora"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Instalação completa!"
echo ""
