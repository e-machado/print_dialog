#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criar imagens de teste para demonstração do programa de impressão
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_test_images(num_images=4, folder="./test_images"):
    """Cria imagens de teste coloridas com texto"""
    
    # Criar pasta
    os.makedirs(folder, exist_ok=True)
    
    # Cores para as imagens
    colors = [
        (255, 100, 100),  # Vermelho
        (100, 255, 100),  # Verde
        (100, 100, 255),  # Azul
        (255, 255, 100),  # Amarelo
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Ciano
    ]
    
    print(f"Criando {num_images} imagens de teste em '{folder}'...\n")
    
    for i in range(1, num_images + 1):
        # Criar imagem
        width, height = 400, 300
        color = colors[i % len(colors)]
        
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        
        # Adicionar texto
        text = f"Imagem #{i}"
        
        # Tentar usar fonte do sistema, senão usar padrão
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calcular posição do texto (centralizado)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 30
        
        # Desenhar texto branco
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # Adicionar informações
        info_text = f"{width}x{height}px"
        try:
            info_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            info_font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), info_text, font=info_font)
        info_width = bbox[2] - bbox[0]
        info_x = (width - info_width) // 2
        info_y = y + 80
        
        draw.text((info_x, info_y), info_text, fill=(255, 255, 255), font=info_font)
        
        # Salvar imagem
        filename = os.path.join(folder, f"teste_{i:02d}.png")
        img.save(filename)
        
        print(f"  ✓ Criada: {filename}")
    
    print(f"\n✓ {num_images} imagens criadas com sucesso!")
    print(f"\nPróximos passos:")
    print(f"1. Execute: python3 print_images_real.py")
    print(f"2. As imagens serão carregadas automaticamente")
    print(f"3. Configure a impressão na interface")
    print(f"4. Clique em 'Visualizar PDF' para ver o layout")
    print(f"5. Clique em 'Imprimir' para enviar para impressora")

if __name__ == "__main__":
    try:
        create_test_images(6, "./test_images")
    except Exception as e:
        print(f"✗ Erro: {e}")
        print("\nVerifique se Pillow está instalado:")
        print("  pip3 install Pillow")
