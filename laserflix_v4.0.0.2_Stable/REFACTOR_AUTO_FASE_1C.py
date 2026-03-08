#!/usr/bin/env python3
"""
REFACTOR_AUTO_FASE_1C.py - Integrar SelectionBar component

FASE-1C: Remove código duplicado de selection_bar e integra componente existente

O que este script faz:
1. Backup de ui_builder.py
2. Remove método _build_selection_bar() de UIBuilder
3. Atualiza main_window.py para usar SelectionBar component
4. Valida sintaxe Python
5. Reporta mudanças

Baseado em: WORKFLOW ABSOLUTO (Regra #0)
Modelo: Claude Sonnet 4.5
Data: 08/03/2026
"""

import os
import re
import ast
from datetime import datetime

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_BUILDER_PATH = os.path.join(BASE_DIR, "ui", "builders", "ui_builder.py")
MAIN_WINDOW_PATH = os.path.join(BASE_DIR, "ui", "main_window.py")

def backup_file(filepath):
    """Cria backup com timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup_FASE_1C_{timestamp}"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Backup criado: {os.path.basename(backup_path)}")
    return backup_path

def validate_python_syntax(filepath):
    """Valida sintaxe Python do arquivo."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        print(f"❌ ERRO DE SINTAXE em {filepath}:")
        print(f"   Linha {e.lineno}: {e.msg}")
        return False

def remove_selection_bar_from_ui_builder():
    """
    Remove método _build_selection_bar() de UIBuilder.
    
    Returns:
        tuple: (success, lines_removed, new_content)
    """
    print("\n🔧 Processando ui_builder.py...")
    
    with open(UI_BUILDER_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_line_count = len(lines)
    
    # Encontrar início e fim do método _build_selection_bar
    inside_method = False
    method_start_idx = None
    method_end_idx = None
    method_indent = None
    
    for i, line in enumerate(lines):
        # Detectar início do método
        if 'def _build_selection_bar(window)' in line:
            inside_method = True
            method_start_idx = i
            method_indent = len(line) - len(line.lstrip())
            print(f"   🔍 Encontrado _build_selection_bar na linha {i+1}")
            continue
        
        # Se estamos dentro do método, procurar próximo método ou fim da classe
        if inside_method:
            stripped = line.lstrip()
            current_indent = len(line) - len(stripped)
            
            # Próximo método (@staticmethod ou def) ou fim do arquivo
            if (stripped.startswith('@staticmethod') or 
                (stripped.startswith('def ') and current_indent == method_indent)):
                method_end_idx = i
                print(f"   🔍 Fim do método na linha {i}")
                break
    
    if method_start_idx is None:
        print("   ⚠️  Método _build_selection_bar não encontrado!")
        return False, 0, None
    
    # Se não encontrou fim explícito, ir até o fim do arquivo
    if method_end_idx is None:
        method_end_idx = len(lines)
    
    # Remover linhas do método
    new_lines = lines[:method_start_idx] + lines[method_end_idx:]
    
    # Remover linhas em branco consecutivas que ficaram
    final_lines = []
    prev_blank = False
    for line in new_lines:
        is_blank = line.strip() == ''
        if not (is_blank and prev_blank):
            final_lines.append(line)
        prev_blank = is_blank
    
    new_content = ''.join(final_lines)
    lines_removed = original_line_count - len(final_lines)
    
    print(f"   ✅ Removidas {lines_removed} linhas do método _build_selection_bar")
    
    return True, lines_removed, new_content

def update_main_window_to_use_component():
    """
    Atualiza main_window.py para usar SelectionBar component.
    
    Mudanças:
    1. Adiciona import de SelectionBar
    2. Atualiza _on_selection_mode_changed para usar component
    3. Atualiza _on_selection_count_changed para usar component
    
    Returns:
        tuple: (success, changes_made, new_content)
    """
    print("\n🔧 Processando main_window.py...")
    
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. Adicionar import se não existir
    if 'from ui.components.selection_bar import SelectionBar' not in content:
        # Encontrar linha de imports de ui.components
        import_pattern = r'(from ui\.builders\.ui_builder import UIBuilder)'
        replacement = r'\1\nfrom ui.components.selection_bar import SelectionBar'
        content = re.sub(import_pattern, replacement, content)
        changes.append("Import SelectionBar adicionado")
        print("   ✅ Import adicionado")
    
    # 2. Adicionar instanciação do SelectionBar no __init__ (antes do display_projects)
    # Procurar onde UIBuilder.build é chamado e adicionar depois
    if 'self.selection_bar = SelectionBar' not in content:
        # Adicionar após UIBuilder.build(self)
        pattern = r'(UIBuilder\.build\(self\))'
        replacement = r'''\1
        
        # SelectionBar component (FASE-1C)
        self.selection_bar = SelectionBar(self.root)'''
        content = re.sub(pattern, replacement, content)
        changes.append("SelectionBar instanciado")
        print("   ✅ SelectionBar instanciado")
    
    # 3. Atualizar _on_selection_mode_changed
    # Substituir _sel_bar.pack/pack_forget por selection_bar.show/hide
    old_mode_changed = r'''def _on_selection_mode_changed\(self, is_active: bool\) -> None:
        if is_active:
            self\._sel_bar\.pack\(fill="x", before=self\.content_canvas\.master\)
            self\.header\.set_select_btn_active\(True\)
        else:
            self\._sel_bar\.pack_forget\(\)
            self\.header\.set_select_btn_active\(False\)'''
    
    new_mode_changed = '''def _on_selection_mode_changed(self, is_active: bool) -> None:
        if is_active:
            self.selection_bar.show()
            self.header.set_select_btn_active(True)
        else:
            self.selection_bar.hide()
            self.header.set_select_btn_active(False)'''
    
    if re.search(old_mode_changed, content):
        content = re.sub(old_mode_changed, new_mode_changed, content)
        changes.append("_on_selection_mode_changed atualizado")
        print("   ✅ _on_selection_mode_changed atualizado")
    
    # 4. Atualizar _on_selection_count_changed
    # Substituir _sel_count_lbl.config por selection_bar.update_count
    old_count_changed = r'''def _on_selection_count_changed\(self, count: int\) -> None:
        self\._sel_count_lbl\.config\(text=f"{count} selecionado\(s\)"\)'''
    
    new_count_changed = '''def _on_selection_count_changed(self, count: int) -> None:
        self.selection_bar.update_count(count)'''
    
    if re.search(old_count_changed, content):
        content = re.sub(old_count_changed, new_count_changed, content)
        changes.append("_on_selection_count_changed atualizado")
        print("   ✅ _on_selection_count_changed atualizado")
    
    if not changes:
        print("   ⚠️  Nenhuma mudança necessária em main_window.py")
        return False, changes, None
    
    return True, changes, content

def main():
    print("🚀 REFACTOR_AUTO_FASE_1C - Integrar SelectionBar")
    print("=" * 60)
    
    # Verificar se arquivos existem
    if not os.path.exists(UI_BUILDER_PATH):
        print(f"❌ Arquivo não encontrado: {UI_BUILDER_PATH}")
        return False
    
    if not os.path.exists(MAIN_WINDOW_PATH):
        print(f"❌ Arquivo não encontrado: {MAIN_WINDOW_PATH}")
        return False
    
    # Criar backups
    print("\n💾 Criando backups...")
    ui_builder_backup = backup_file(UI_BUILDER_PATH)
    main_window_backup = backup_file(MAIN_WINDOW_PATH)
    
    # Processar ui_builder.py
    success_builder, lines_removed_builder, new_builder_content = remove_selection_bar_from_ui_builder()
    
    if not success_builder:
        print("\n❌ Falha ao processar ui_builder.py")
        return False
    
    # Processar main_window.py
    success_main, changes_main, new_main_content = update_main_window_to_use_component()
    
    if not success_main:
        print("\n⚠️  main_window.py não precisou de mudanças (pode já estar correto)")
    
    # Escrever novos conteúdos
    print("\n📝 Aplicando mudanças...")
    
    with open(UI_BUILDER_PATH, 'w', encoding='utf-8') as f:
        f.write(new_builder_content)
    print(f"   ✅ ui_builder.py atualizado")
    
    if new_main_content:
        with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
            f.write(new_main_content)
        print(f"   ✅ main_window.py atualizado")
    
    # Validar sintaxe
    print("\n🔍 Validando sintaxe Python...")
    
    if not validate_python_syntax(UI_BUILDER_PATH):
        print("\n❌ Erro de sintaxe em ui_builder.py! Revertendo...")
        with open(ui_builder_backup, 'r', encoding='utf-8') as f:
            with open(UI_BUILDER_PATH, 'w', encoding='utf-8') as out:
                out.write(f.read())
        return False
    
    if new_main_content and not validate_python_syntax(MAIN_WINDOW_PATH):
        print("\n❌ Erro de sintaxe em main_window.py! Revertendo...")
        with open(main_window_backup, 'r', encoding='utf-8') as f:
            with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as out:
                out.write(f.read())
        return False
    
    print("   ✅ Sintaxe validada com sucesso!")
    
    # Relatório final
    print("\n" + "=" * 60)
    print("✅ FASE-1C CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print(f"\n📄 Arquivos modificados:")
    print(f"   1. ui/builders/ui_builder.py (-{lines_removed_builder} linhas)")
    if changes_main:
        print(f"   2. ui/main_window.py ({len(changes_main)} mudanças)")
        for change in changes_main:
            print(f"      - {change}")
    
    print(f"\n💾 Backups criados:")
    print(f"   - {os.path.basename(ui_builder_backup)}")
    print(f"   - {os.path.basename(main_window_backup)}")
    
    print(f"\n🧪 PRÓXIMOS PASSOS:")
    print(f"   1. Testar o app: python main.py")
    print(f"   2. Verificar modo de seleção (botão no header)")
    print(f"   3. Confirmar que barra de seleção aparece/desaparece")
    print(f"   4. Testar botões: Selecionar tudo, Deselecionar, Remover, Cancelar")
    print(f"   5. Se tudo OK, fazer commit")
    
    print(f"\n💡 Sugestão de commit:")
    print(f'   git add .')
    print(f'   git commit -m "refactor(FASE-1C): integrate SelectionBar component (-{lines_removed_builder} lines)"')
    print(f'   git push origin main')
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
