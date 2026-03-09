#!/usr/bin/env python3
"""
apply_patch_selection_ux.py - SCRIPT DEFINITIVO para Selection UX Refactor.

Versão final testada e validada.

Usage:
    python apply_patch_selection_ux.py
"""

import os
import re
import shutil
import ast
import sys
from datetime import datetime


MAIN_WINDOW_PATH = "ui/main_window.py"
BACKUP_SUFFIX = f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def create_backup(filepath):
    """Cria backup do arquivo."""
    backup_path = filepath + BACKUP_SUFFIX
    shutil.copy2(filepath, backup_path)
    print(f"✅ Backup criado: {backup_path}")
    return backup_path


def read_file(filepath):
    """Lê conteúdo do arquivo."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    """Escreve conteúdo no arquivo."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def validate_python_syntax(content):
    """Valida se o conteúdo é Python válido."""
    try:
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Linha {e.lineno}: {e.msg}"


def apply_patch(content):
    """
    Aplica todas as mudanças necessárias.
    
    Returns:
        (modified_content, changes_applied)
    """
    changes = []
    original = content
    
    # 1. ADICIONAR import SelectionBarManager
    if "from ui.managers.selection_bar_manager import SelectionBarManager" not in content:
        pattern = r"(from ui\.managers\.modal_generator import ModalGenerator)"
        replacement = r"\1\nfrom ui.managers.selection_bar_manager import SelectionBarManager"
        content = re.sub(pattern, replacement, content, count=1)
        if content != original:
            changes.append("✅ Import SelectionBarManager adicionado")
            original = content
    
    # 2. INSTANCIAR SelectionBarManager após _build_ui()
    if "self.selection_bar_mgr = SelectionBarManager" not in content:
        pattern = r"(self\._build_ui\(\)\n)(\s*\n\s*# === MANAGERS \(criados DEPOIS de UI existir\) ===)"
        replacement = (
            r"\1\n"
            r"        # === MANAGERS (criados DEPOIS de UI existir) ===\n"
            r"        # UX-REFACTOR: SelectionBarManager (auto show/hide)\n"
            r"        self.selection_bar_mgr = SelectionBarManager(\n"
            r"            parent_frame=self._content_frame,\n"
            r"            selection_ctrl=self.selection_ctrl,\n"
            r"            display_ctrl=self.display_ctrl,\n"
            r"            root=self.root\n"
            r"        )\n"
        )
        content = re.sub(pattern, replacement, content, count=1)
        if content != original:
            changes.append("✅ SelectionBarManager instanciado")
            original = content
    
    # 3. REMOVER on_mode_changed callback (linha completa)
    pattern = r"^\s*self\.selection_ctrl\.on_mode_changed = self\._on_selection_mode_changed\s*\n"
    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, "", content, flags=re.MULTILINE)
        changes.append("✅ Callback on_mode_changed removido")
        original = content
    
    # 4. REMOVER on_selection_changed (REMOVER COMPLETAMENTE, NÃO COMENTAR!)
    pattern = r"^\s*self\.selection_ctrl\.on_selection_changed = self\._on_selection_count_changed\s*\n"
    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, "", content, flags=re.MULTILINE)
        changes.append("✅ Callback on_selection_changed REMOVIDO")
        original = content
    
    # 5. REMOVER callback on_projects_removed (se existir com lambda)
    pattern = r"^\s*self\.selection_ctrl\.on_projects_removed = lambda count:.*?\n"
    if re.search(pattern, content, re.MULTILINE):
        # NÃO remover, ele é usado
        pass
    
    # 6. REMOVER método _on_selection_mode_changed (bloco completo)
    pattern = r"\n    # SELECTION CALLBACKS\n    def _on_selection_mode_changed\(self, is_active: bool\) -> None:.*?(?=\n    def |\n    # [A-Z]|\Z)"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, "", content, flags=re.DOTALL, count=1)
        changes.append("✅ Método _on_selection_mode_changed removido")
        original = content
    
    # 7. REMOVER método _on_selection_count_changed
    pattern = r"\n    def _on_selection_count_changed\(self, count: int\) -> None:.*?(?=\n    def |\n    # [A-Z]|\Z)"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, "", content, flags=re.DOTALL, count=1)
        changes.append("✅ Método _on_selection_count_changed removido")
        original = content
    
    # 8. REMOVER selection_mode de _should_rebuild()
    pattern = r'^(\s*)current_state\["selection_mode"\] = self\.selection_ctrl\.selection_mode\s*\n'
    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, "", content, flags=re.MULTILINE, count=1)
        changes.append("✅ selection_mode removido de _should_rebuild()")
        original = content
    
    # 9. REMOVER selection_mode de _get_card_callbacks()
    pattern = r'^(\s*)"selection_mode": self\.selection_ctrl\.selection_mode,\s*\n'
    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, "", content, flags=re.MULTILINE, count=1)
        changes.append("✅ selection_mode removido de _get_card_callbacks()")
        original = content
    
    # 10. REMOVER verificação selection_mode em open_project_modal()
    pattern = r"(def open_project_modal\(self, project_path: str\) -> None:\n)(\s+)if self\.selection_ctrl\.selection_mode:\n\s+self\.selection_ctrl\.toggle_project\(project_path\); return\n"
    if re.search(pattern, content):
        replacement = r"\1"
        content = re.sub(pattern, replacement, content, count=1)
        changes.append("✅ Verificação selection_mode removida de open_project_modal()")
        original = content
    
    return content, changes


def validate_patch(content):
    """Valida se patch foi aplicado corretamente."""
    errors = []
    
    # Verificações obrigatórias
    if "from ui.managers.selection_bar_manager import SelectionBarManager" not in content:
        errors.append("❌ Import SelectionBarManager não encontrado")
    
    if "self.selection_bar_mgr = SelectionBarManager" not in content:
        errors.append("❌ SelectionBarManager não instanciado")
    
    # Verificações de limpeza
    if "def _on_selection_mode_changed" in content:
        errors.append("❌ Método _on_selection_mode_changed ainda presente")
    
    if "def _on_selection_count_changed" in content:
        errors.append("❌ Método _on_selection_count_changed ainda presente")
    
    if '"selection_mode": self.selection_ctrl.selection_mode' in content:
        errors.append("❌ selection_mode ainda em _get_card_callbacks()")
    
    if "self.selection_ctrl.on_mode_changed" in content:
        errors.append("❌ Callback on_mode_changed ainda presente")
    
    if "self.selection_ctrl.on_selection_changed = self._on_selection_count_changed" in content:
        errors.append("❌ Callback on_selection_changed ainda presente (ERRO FATAL!)")
    
    # Validar sintaxe Python
    is_valid, syntax_error = validate_python_syntax(content)
    if not is_valid:
        errors.append(f"❌ ERRO DE SINTAXE: {syntax_error}")
    
    return errors


def main():
    print("\n🚀 APLICANDO PATCH DEFINITIVO: Selection UX Refactor\n")
    print("="*60)
    
    # Verificar se arquivo existe
    if not os.path.exists(MAIN_WINDOW_PATH):
        print(f"\n❌ Arquivo não encontrado: {MAIN_WINDOW_PATH}")
        print("   Execute este script na pasta laserflix_v4.0.0.6_Stable/")
        return 1
    
    # Criar backup
    print("\n💾 Criando backup...")
    backup_path = create_backup(MAIN_WINDOW_PATH)
    
    # Ler arquivo
    print(f"\n📄 Lendo {MAIN_WINDOW_PATH}...")
    content = read_file(MAIN_WINDOW_PATH)
    original_lines = content.count('\n')
    
    # Aplicar patch
    print("\n⚙️  Aplicando mudanças...\n")
    modified_content, changes = apply_patch(content)
    
    # Mostrar mudanças aplicadas
    if changes:
        for change in changes:
            print(f"  {change}")
    else:
        print("  ⚠️  Nenhuma mudança necessária (patch já aplicado?)")
    
    # Validar
    print("\n✅ Validando patch...")
    errors = validate_patch(modified_content)
    
    if errors:
        print("\n❌ VALIDAÇÃO FALHOU:\n")
        for error in errors:
            print(f"  {error}")
        print(f"\n🔄 Nada foi modificado. Backup: {backup_path}")
        return 1
    
    # Escrever arquivo modificado
    write_file(MAIN_WINDOW_PATH, modified_content)
    modified_lines = modified_content.count('\n')
    
    # Resumo
    print("\n" + "="*60)
    print("✅ PATCH APLICADO COM SUCESSO!\n")
    print(f"📊 Estatísticas:")
    print(f"  • Linhas originais: {original_lines}")
    print(f"  • Linhas finais: {modified_lines}")
    print(f"  • Diferença: {modified_lines - original_lines:+d} linhas")
    print(f"  • Mudanças aplicadas: {len(changes)}")
    print(f"\n💾 Backup: {backup_path}")
    print(f"\n✅ Pronto! Execute: python main.py")
    print("="*60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
