#!/bin/bash

# Print Dialog - Script de Instalação Automática
# Detecta a distribuição Linux e instala dependências automaticamente

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_header() {
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Print Dialog - Script de Instalação${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Detectar distribuição Linux
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        echo "$DISTRIB_ID" | tr '[:upper:]' '[:lower:]'
    else
        echo "unknown"
    fi
}

# Instalar para Debian/Ubuntu
install_debian() {
    print_info "Detectado: Debian/Ubuntu"
    
    print_info "Atualizando lista de pacotes..."
    sudo apt-get update
    
    print_info "Instalando dependências..."
    sudo apt-get install -y python3 python3-tk python3-pip
    
    print_info "Instalando Pillow..."
    pip3 install --user Pillow
    
    print_success "Dependências instaladas!"
    
    print_info "Instalando PyQt5 (opcional)..."
    read -p "Deseja instalar PyQt5 para versão profissional? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo apt-get install -y python3-pyqt5
        print_success "PyQt5 instalado!"
    fi
}

# Instalar para Fedora/RHEL
install_fedora() {
    print_info "Detectado: Fedora/RHEL/CentOS"
    
    print_info "Instalando dependências..."
    sudo dnf install -y python3 python3-tkinter python3-pip
    
    print_info "Instalando Pillow..."
    pip3 install --user Pillow
    
    print_success "Dependências instaladas!"
    
    print_info "Instalando PyQt5 (opcional)..."
    read -p "Deseja instalar PyQt5 para versão profissional? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo dnf install -y python3-pyqt5
        print_success "PyQt5 instalado!"
    fi
}

# Instalar para Arch
install_arch() {
    print_info "Detectado: Arch Linux"
    
    print_info "Instalando dependências..."
    sudo pacman -S --noconfirm python tk python-pip
    
    print_info "Instalando Pillow..."
    pip install --user Pillow
    
    print_success "Dependências instaladas!"
    
    print_info "Instalando PyQt5 (opcional)..."
    read -p "Deseja instalar PyQt5 para versão profissional? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo pacman -S --noconfirm python-pyqt5
        print_success "PyQt5 instalado!"
    fi
}

# Instalar para Alpine
install_alpine() {
    print_info "Detectado: Alpine Linux"
    
    print_info "Instalando dependências..."
    sudo apk add --no-cache python3 py3-tk py3-pip
    
    print_info "Instalando Pillow..."
    pip3 install --user Pillow
    
    print_success "Dependências instaladas!"
}

# Instalar para OpenSUSE
install_opensuse() {
    print_info "Detectado: openSUSE"
    
    print_info "Instalando dependências..."
    sudo zypper install -y python3 python3-tk python3-pip
    
    print_info "Instalando Pillow..."
    pip3 install --user Pillow
    
    print_success "Dependências instaladas!"
    
    print_info "Instalando PyQt5 (opcional)..."
    read -p "Deseja instalar PyQt5 para versão profissional? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo zypper install -y python3-PyQt5
        print_success "PyQt5 instalado!"
    fi
}

# Menu de seleção manual
install_manual() {
    print_warning "Não foi possível detectar a distribuição automaticamente."
    echo ""
    echo "Selecione sua distribuição:"
    echo "1) Debian/Ubuntu"
    echo "2) Fedora/RHEL/CentOS"
    echo "3) Arch Linux"
    echo "4) Alpine"
    echo "5) openSUSE"
    echo "6) Outra (instalação manual)"
    echo ""
    read -p "Escolha (1-6): " choice
    
    case $choice in
        1) install_debian ;;
        2) install_fedora ;;
        3) install_arch ;;
        4) install_alpine ;;
        5) install_opensuse ;;
        6)
            print_info "Instalação manual:"
            print_info "1. Instale Python 3: sudo apt-get install python3"
            print_info "2. Instale tkinter: sudo apt-get install python3-tk"
            print_info "3. Instale pip: sudo apt-get install python3-pip"
            print_info "4. Instale Pillow: pip3 install Pillow"
            print_info "5. (Opcional) Instale PyQt5: pip3 install PyQt5"
            ;;
        *)
            print_error "Opção inválida!"
            exit 1
            ;;
    esac
}

# Criar links simbólicos e tornar executável
setup_executable() {
    print_info "Configurando executáveis..."
    
    if [ -f "print_dialog.py" ]; then
        chmod +x print_dialog.py
        print_success "print_dialog.py é executável"
    fi
    
    if [ -f "print_dialog_pyqt5.py" ]; then
        chmod +x print_dialog_pyqt5.py
        print_success "print_dialog_pyqt5.py é executável"
    fi
}

# Menu inicial
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1) Instalar dependências (automático)"
    echo "2) Instalar dependências (manual)"
    echo "3) Verificar instalação"
    echo "4) Executar Print Dialog (tkinter)"
    echo "5) Executar Print Dialog (PyQt5)"
    echo "6) Sair"
    echo ""
    read -p "Escolha (1-6): " option
    
    case $option in
        1)
            distro=$(detect_distro)
            case $distro in
                debian|ubuntu) install_debian ;;
                fedora|rhel|centos) install_fedora ;;
                arch) install_arch ;;
                alpine) install_alpine ;;
                opensuse|opensuse-leap|opensuse-tumbleweed) install_opensuse ;;
                *) install_manual ;;
            esac
            setup_executable
            show_menu
            ;;
        2)
            install_manual
            setup_executable
            show_menu
            ;;
        3)
            verify_installation
            show_menu
            ;;
        4)
            if [ -f "print_dialog.py" ]; then
                print_info "Iniciando Print Dialog (tkinter)..."
                python3 print_dialog.py
            else
                print_error "Arquivo print_dialog.py não encontrado!"
            fi
            show_menu
            ;;
        5)
            if [ -f "print_dialog_pyqt5.py" ]; then
                print_info "Iniciando Print Dialog (PyQt5)..."
                python3 print_dialog_pyqt5.py
            else
                print_error "Arquivo print_dialog_pyqt5.py não encontrado!"
            fi
            show_menu
            ;;
        6)
            print_info "Saindo..."
            exit 0
            ;;
        *)
            print_error "Opção inválida!"
            show_menu
            ;;
    esac
}

# Verificar instalação
verify_installation() {
    echo ""
    print_info "Verificando instalação..."
    
    # Python
    if command -v python3 &> /dev/null; then
        version=$(python3 --version)
        print_success "Python 3 instalado: $version"
    else
        print_error "Python 3 não encontrado"
    fi
    
    # tkinter
    if python3 -c "import tkinter" 2>/dev/null; then
        print_success "tkinter instalado"
    else
        print_error "tkinter não instalado"
    fi
    
    # Pillow
    if python3 -c "import PIL" 2>/dev/null; then
        print_success "Pillow instalado"
    else
        print_error "Pillow não instalado"
    fi
    
    # PyQt5
    if python3 -c "import PyQt5" 2>/dev/null; then
        print_success "PyQt5 instalado"
    else
        print_warning "PyQt5 não instalado (opcional)"
    fi
    
    echo ""
}

# Programa principal
main() {
    print_header
    
    # Verificar se é root
    if [[ $EUID -eq 0 ]]; then
        print_warning "Este script não deve ser executado como root"
        exit 1
    fi
    
    # Verificar se está em um repositório git/diretório de trabalho
    if [ ! -f "print_dialog.py" ]; then
        print_warning "Execute este script no diretório contendo os arquivos Print Dialog"
        print_info "Ou especifique o diretório:"
        print_info "cd /caminho/para/print-dialog && ./install.sh"
        exit 1
    fi
    
    show_menu
}

# Executar programa principal
main
