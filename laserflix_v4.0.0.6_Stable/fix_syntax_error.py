#!/usr/bin/env python3
"""
fix_syntax_error.py - Corrige erro de sintaxe deixado pelo patch.

O problema: linha 118 tem ')        self.selection_ctrl...'
A solução: remover o ')' extra no início da linha.
"""

import re

MAIN_WINDOW_PATH = "ui/main_window.py"

def fix_syntax_error():
    print("\n🔧 CORRIGINDO ERRO DE SINTAXE...\n")
    
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrigir linha com ) solto
    # Padrão: )        self.selection_ctrl.on_selection_changed
    pattern = r"\)\s+(self\.selection_ctrl\.on_selection_changed)"
    
    if re.search(pattern, content):
        content = re.sub(pattern, r"\1", content)
        print("✅ Removido ')' extra da linha 118")
    else:
        print("⚠️  Padrão não encontrado, tentando abordagem alternativa...")
        
        # Abordagem alternativa: remover linha com apenas )
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Pular linhas que são apenas ')' seguido de espaços
            if line.strip() == ')' and i > 0 and 'self.selection_ctrl' in lines[i+1]:
                print(f"✅ Removida linha {i+1} com ')' solto")
                continue
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
    
    # Escrever arquivo corrigido
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Erro corrigido!")
    print("\n✅ Agora execute: python main.py")

if __name__ == "__main__":
    fix_syntax_error()
