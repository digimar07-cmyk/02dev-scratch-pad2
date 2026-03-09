#!/usr/bin/env python3
"""
apply_selection_ux_patch.py - Aplica patch automático para Selection UX Refactor.

Este script modifica main_window.py automaticamente para integrar o novo
SelectionBarManager.

Usage:
    python apply_selection_ux_patch.py

O que faz:
1. Cria backup de main_window.py
2. Adiciona import de SelectionBarManager
3. Instancia SelectionBarManager no __init__
4. Remove callbacks e métodos obsoletos
5. Remove referências a selection_mode
6. Valida aplicação bem-sucedida
"""

import os
import re
import shutil
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


def apply_patch(content):
    """
    Aplica todas as mudanças necessárias.
    
    Returns:
        (modified_content, changes_applied)
    """
    changes = []
    
    # 1. ADICIONAR import SelectionBarManager
    if "from ui.managers.selection_bar_manager import SelectionBarManager" not in content:
        # Encontrar bloco de imports de ui.managers
        import_pattern = r"(from ui\.managers\.orphan_manager import OrphanManager)"
        replacement = r"\1\nfrom ui.managers.selection_bar_manager import SelectionBarManager"
        content = re.sub(import_pattern, replacement, content)
        changes.append("✅ Import SelectionBarManager adicionado")
    
    # 2. INSTANCIAR SelectionBarManager após _build_ui()
    if "self.selection_bar_mgr = SelectionBarManager" not in content:
        # Encontrar linha self._build_ui()
        pattern = r"(self\._build_ui\(\)\s*\n\s*\n\s*# === MANAGERS)"
        replacement = (
            r"self._build_ui()\n"
            r"\n"
            r"        # === MANAGERS (criados DEPOIS de UI existir) ===\n"
            r"        # UX-REFACTOR: SelectionBarManager (auto show/hide)\n"
            r"        self.selection_bar_mgr = SelectionBarManager(\n"
            r"            parent_frame=self._content_frame,\n"
            r"            selection_ctrl=self.selection_ctrl,\n"
            r"            display_ctrl=self.display_ctrl,\n"
            r"            root=self.root\n"
            r"        )\n"
            r"        \n"
            r"        # === MANAGERS"
        )
        content = re.sub(pattern, replacement, content)
        changes.append("✅ SelectionBarManager instanciado")
    
    # 3. REMOVER on_mode_changed callback
    pattern = r"\s*self\.selection_ctrl\.on_mode_changed = self\._on_selection_mode_changed\s*\n"
    if re.search(pattern, content):
        content = re.sub(pattern, "", content)
        changes.append("✅ on_mode_changed callback removido")
    
    # 4. REMOVER on_selection_changed callback (opcional, manager cuida)
    # Comentar ao invés de remover (para segurança)
    pattern = r"(\s*)(self\.selection_ctrl\.on_selection_changed = self\._on_selection_count_changed)"
    if re.search(pattern, content) and "# UX-REFACTOR" not in content:
        replacement = r"\1# UX-REFACTOR: Gerenciado por SelectionBarManager\n\1# \2"
        content = re.sub(pattern, replacement, content)
        changes.append("✅ on_selection_changed callback comentado")
    
    # 5. REMOVER métodos _on_selection_mode_changed e _on_selection_count_changed
    # Método 1: _on_selection_mode_changed
    pattern1 = r"\s*# SELECTION CALLBACKS\s*\n\s*def _on_selection_mode_changed\(self, is_active: bool\) -> None:.*?(?=\n    def |\n    # |\Z)"
    if re.search(pattern1, content, re.DOTALL):
        content = re.sub(pattern1, "", content, flags=re.DOTALL)
        changes.append("✅ Método _on_selection_mode_changed removido")
    
    # Método 2: _on_selection_count_changed
    pattern2 = r"\s*def _on_selection_count_changed\(self, count: int\) -> None:.*?(?=\n    def |\n    # |\Z)"
    if re.search(pattern2, content, re.DOTALL):
        content = re.sub(pattern2, "", content, flags=re.DOTALL)
        changes.append("✅ Método _on_selection_count_changed removido")
    
    # 6. REMOVER selection_mode de _should_rebuild()
    pattern = r'\s*current_state\["selection_mode"\] = self\.selection_ctrl\.selection_mode\s*\n'
    if re.search(pattern, content):
        replacement = "        # UX-REFACTOR: selection_mode removido (não existe mais)\n"
        content = re.sub(pattern, replacement, content)
        changes.append("✅ selection_mode removido de _should_rebuild()")
    
    # 7. REMOVER selection_mode de _get_card_callbacks()
    pattern = r'\s*"selection_mode": self\.selection_ctrl\.selection_mode,\s*\n'
    if re.search(pattern, content):
        replacement = "            # UX-REFACTOR: selection_mode removido (checkboxes sempre visíveis)\n"
        content = re.sub(pattern, replacement, content)
        changes.append("✅ selection_mode removido de _get_card_callbacks()")
    
    # 8. REMOVER verificação de selection_mode em open_project_modal()
    pattern = r"(def open_project_modal\(self, project_path: str\) -> None:\s*\n)\s*if self\.selection_ctrl\.selection_mode:\s*\n\s*self\.selection_ctrl\.toggle_project\(project_path\); return\s*\n"
    if re.search(pattern, content):
        replacement = r"\1        # UX-REFACTOR: Sempre abre modal, checkbox é independente\n"
        content = re.sub(pattern, replacement, content)
        changes.append("✅ Verificação selection_mode removida de open_project_modal()")
    
    return content, changes


def validate_patch(content):
    """Valida se patch foi aplicado corretamente."""
    errors = []
    
    if "from ui.managers.selection_bar_manager import SelectionBarManager" not in content:
        errors.append("❌ Import SelectionBarManager não encontrado")
    
    if "self.selection_bar_mgr = SelectionBarManager" not in content:
        errors.append("❌ SelectionBarManager não instanciado")
    
    if "self.selection_ctrl.on_mode_changed" in content and "# UX-REFACTOR" not in content:
        errors.append("❌ on_mode_changed ainda presente")
    
    if "def _on_selection_mode_changed" in content:
        errors.append("❌ Método _on_selection_mode_changed ainda presente")
    
    if '"selection_mode": self.selection_ctrl.selection_mode' in content:
        errors.append("❌ selection_mode ainda presente em _get_card_callbacks()")
    
    return errors


def main():
    print("\n🚀 APLICANDO PATCH: Selection UX Refactor\n")
    
    # Verificar se arquivo existe
    if not os.path.exists(MAIN_WINDOW_PATH):
        print(f"❌ Arquivo não encontrado: {MAIN_WINDOW_PATH}")
        print("   Execute este script na pasta laserflix_v4.0.0.6_Stable/")
        return 1
    
    # Criar backup
    backup_path = create_backup(MAIN_WINDOW_PATH)
    
    # Ler arquivo
    print(f"\n📄 Lendo {MAIN_WINDOW_PATH}...")
    content = read_file(MAIN_WINDOW_PATH)
    original_lines = content.count('\n')
    
    # Aplicar patch
    print("\n⚙️ Aplicando mudanças...\n")
    modified_content, changes = apply_patch(content)
    
    # Mostrar mudanças aplicadas
    for change in changes:
        print(f"  {change}")
    
    if not changes:
        print("  ⚠️  Nenhuma mudança necessária (patch já aplicado?)")
        return 0
    
    # Validar
    print("\n✅ Validando patch...\n")
    errors = validate_patch(modified_content)
    
    if errors:
        print("❌ VALIDAÇÃO FALHOU:\n")
        for error in errors:
            print(f"  {error}")
        print(f"\n🔄 Backup disponível em: {backup_path}")
        return 1
    
    # Escrever arquivo modificado
    write_file(MAIN_WINDOW_PATH, modified_content)
    modified_lines = modified_content.count('\n')
    
    # Resumo
    print("✅ Patch aplicado com sucesso!\n")
    print(f"📊 Estatísticas:")
    print(f"  - Linhas originais: {original_lines}")
    print(f"  - Linhas finais: {modified_lines}")
    print(f"  - Diferença: {modified_lines - original_lines:+d} linhas")
    print(f"  - Mudanças aplicadas: {len(changes)}")
    print(f"\n💾 Backup salvo em: {backup_path}")
    print(f"\n✅ Pronto para testar! Execute: python main.py")
    
    return 0


if __name__ == "__main__":
    exit(main())
