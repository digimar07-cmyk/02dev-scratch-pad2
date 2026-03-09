"""
ui/managers/selection_bar_manager.py — Gerencia barra de seleção automática.

UX-REFACTOR: Barra aparece automaticamente quando há seleções.
FASE-3: Extração total de lógica de seleção para fora do main_window.py

Responsabilidades:
- Inicializar SelectionBar component
- Conectar callbacks do SelectionController
- Auto show/hide baseado em contagem
- Atualizar contador visual
"""
import tkinter as tk
from ui.components.selection_bar import SelectionBar


class SelectionBarManager:
    """
    Manager para controle automático da barra de seleção.
    
    UX-REFACTOR: Barra aparece quando count > 0, esconde quando count = 0.
    
    Conecta:
    - SelectionBar (component) para UI
    - SelectionController para lógica
    - DisplayController para obter projetos visíveis
    """
    
    def __init__(self, parent_frame, selection_ctrl, display_ctrl, root):
        """
        Inicializa manager de barra de seleção.
        
        Args:
            parent_frame: Frame pai onde a barra será inserida (content_frame)
            selection_ctrl: SelectionController instance
            display_ctrl: DisplayController instance (para pegar projetos filtrados)
            root: Root window (para passar ao remove_selected)
        """
        self.parent_frame = parent_frame
        self.selection_ctrl = selection_ctrl
        self.display_ctrl = display_ctrl
        self.root = root
        
        # Criar SelectionBar component
        self.selection_bar = SelectionBar(parent_frame)
        
        # Conectar callbacks do SelectionBar aos métodos do SelectionController
        self.selection_bar.on_select_all = self._on_select_all
        self.selection_bar.on_deselect_all = self._on_deselect_all
        self.selection_bar.on_remove_selected = self._on_remove_selected
        self.selection_bar.on_cancel = self._on_cancel
        
        # Conectar callback de mudança de contagem do SelectionController
        self.selection_ctrl.on_selection_changed = self._on_selection_changed
        
        # Estado inicial: escondido
        self.selection_bar.hide()
    
    def _on_select_all(self):
        """Seleciona todos os projetos visíveis na página atual."""
        # Pegar projetos filtrados e visíveis
        filtered_paths = self.display_ctrl.get_filtered_projects()
        self.selection_ctrl.select_all(filtered_paths)
    
    def _on_deselect_all(self):
        """Remove todas as seleções."""
        self.selection_ctrl.deselect_all()
    
    def _on_remove_selected(self):
        """Remove projetos selecionados do banco."""
        self.selection_ctrl.remove_selected(self.root)
    
    def _on_cancel(self):
        """Cancela seleção (deseleciona tudo e esconde barra)."""
        self.selection_ctrl.deselect_all()
    
    def _on_selection_changed(self, count: int):
        """
        Callback chamado quando contagem de seleções muda.
        
        UX-REFACTOR: Auto show/hide baseado em count.
        
        Args:
            count: Número de projetos selecionados
        """
        # Atualizar contador visual
        self.selection_bar.update_count(count)
        
        # Auto show/hide
        if count > 0:
            if not self.selection_bar.is_visible():
                self.selection_bar.show()
        else:
            if self.selection_bar.is_visible():
                self.selection_bar.hide()
    
    def get_count_label(self):
        """Retorna label de contagem (para compatibilidade com código legado)."""
        return self.selection_bar.count_label
    
    def get_frame(self):
        """Retorna frame da barra (para compatibilidade com código legado)."""
        return self.selection_bar.frame
