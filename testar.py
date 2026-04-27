#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste - Verifica se tudo está funcionando
"""

import sys
import os

def test_python_version():
    """Verifica versão do Python"""
    print("🔍 Verificando Python...")
    version = sys.version_info
    print(f"   Versão: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 6:
        print("   ✅ Versão OK")
        return True
    else:
        print("   ❌ Python 3.6+ é necessário")
        return False

def test_module(module_name, display_name, required=True):
    """Testa se um módulo está instalado"""
    try:
        __import__(module_name)
        print(f"   ✅ {display_name}")
        return True
    except ImportError:
        status = "❌ OBRIGATÓRIO" if required else "⚠️  OPCIONAL"
        print(f"   {status} {display_name}")
        return not required

def test_tkinter():
    """Testa tkinter especificamente"""
    print("\n🔍 Verificando tkinter...")
    try:
        import tkinter
        print("   ✅ tkinter")
        return True
    except ImportError:
        print("   ❌ OBRIGATÓRIO tkinter")
        print("      Instale com: sudo apt-get install python3-tk")
        return False

def test_cups():
    """Testa integração com CUPS"""
    print("\n🔍 Verificando CUPS...")
    
    # Verificar módulo
    try:
        import cups
        print("   ✅ Módulo python-cups")
        
        # Tentar conectar
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
            print(f"   ✅ Conexão CUPS ({len(printers)} impressoras)")
            
            for printer in printers:
                print(f"      • {printer}")
            
            return True
        except Exception as e:
            print(f"   ⚠️  Módulo instalado mas não conecta: {e}")
            return True  # Módulo funciona, é só não conseguir conectar
    except ImportError:
        print("   ⚠️  OPCIONAL python-cups")
        print("      Instale com: sudo apt-get install python3-cups")
        print("      (Sem CUPS, modo simulação PDF funcionará)")
        return True

def test_dependencies():
    """Testa dependências Python"""
    print("\n🔍 Verificando Dependências Python...")
    
    deps = [
        ("PIL", "Pillow (manipulação de imagens)", True),
        ("reportlab", "reportlab (geração de PDF)", True),
        ("cups", "python-cups (impressoras)", False),
    ]
    
    all_ok = True
    for module, display, required in deps:
        if not test_module(module, display, required):
            all_ok = False
    
    return all_ok

def test_images():
    """Verifica se há imagens na pasta"""
    print("\n🔍 Verificando Imagens...")
    
    current_dir = os.getcwd()
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
    
    images = []
    try:
        for file in os.listdir(current_dir):
            if os.path.splitext(file)[1].lower() in image_extensions:
                images.append(file)
    except Exception as e:
        print(f"   ❌ Erro ao listar pasta: {e}")
        return False
    
    if images:
        print(f"   ✅ {len(images)} imagem(ns) encontrada(s):")
        for img in images[:5]:  # Mostrar apenas primeiras 5
            print(f"      • {img}")
        if len(images) > 5:
            print(f"      ... e mais {len(images) - 5}")
        return True
    else:
        print("   ⚠️  Nenhuma imagem encontrada na pasta atual")
        print(f"      Pasta: {current_dir}")
        print("      Use: python3 criar_imagens_teste.py")
        return False

def test_permissions():
    """Verifica permissões"""
    print("\n🔍 Verificando Permissões...")
    
    # Verificar se pode escrever
    try:
        test_file = ".test_write"
        with open(test_file, 'w') as f:
            f.write("teste")
        os.remove(test_file)
        print("   ✅ Pode escrever na pasta")
        return True
    except Exception as e:
        print(f"   ❌ Erro de escrita: {e}")
        return False

def print_summary(results):
    """Imprime sumário final"""
    print("\n" + "="*50)
    print("📋 SUMÁRIO")
    print("="*50)
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n✅ TUDO OK! Você pode executar:")
        print("   python3 print_images_real.py")
    else:
        print("\n⚠️  Alguns problemas encontrados:")
        print("\nPara resolver:")
        print("   ./install_print.sh")
        
        if not results['images']:
            print("\nPara testar com imagens de exemplo:")
            print("   python3 criar_imagens_teste.py")
            print("   cd test_images")
            print("   python3 ../print_images_real.py")

def main():
    print("\n" + "🔧 "*15)
    print("TESTE DO SISTEMA DE IMPRESSÃO")
    print("🔧 "*15 + "\n")
    
    results = {}
    
    # Testes
    results['python'] = test_python_version()
    results['tkinter'] = test_tkinter()
    results['dependencies'] = test_dependencies()
    results['cups'] = test_cups()
    results['images'] = test_images()
    results['permissions'] = test_permissions()
    
    # Sumário
    print_summary(results)
    
    print("\n" + "="*50)
    print("Para mais detalhes, veja: README_PRINCIPAL.md")
    print("="*50 + "\n")
    
    # Retornar código de saída
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
