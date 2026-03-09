"""
ui/controllers/selection_controller.py - Gerencia selecao multipla de projetos.

FASE 7C.1: Extrai toda logica de selecao do main_window.py
Reducao estimada: -80 linhas no main_window.py

FIX-SELECTION-FLICKER: on_card_toggled(path, is_selected) para atualização
visual cirúrgica sem rebuild da tela inteira.

FIX-REMOVE: db_manager.save() → save_database() (método correto).
"""

import os
from tkinter import messagebox


class SelectionController:
    """
    Controller para gerenciar selecao multipla de projetos.
    
    Responsabilidades:
    - Ativar/desativar modo selecao
    - Adicionar/remover projetos da selecao
    - Remover projetos selecionados do banco
    """
    
    def __init__(self, database, db_manager, collections_manager):
        self.database = database
        self.db_manager = db_manager
        self.collections_manager = collections_manager
        
        # Estado
        self.selection_mode = False
        self.selected_paths = set()
        
        # Callbacks para UI (main_window conectara)
        self.on_mode_changed = None      # callback(bool: is_active)
        self.on_selection_changed = None # callback(int: count)
        self.on_card_toggled = None      # callback(path: str, is_selected: bool) — FIX-SELECTION-FLICKER
        self.on_projects_removed = None  # callback(int: count)
        self.on_refresh_needed = None    # callback()
    
    def toggle_mode(self):
        """Ativa/desativa modo selecao."""
        self.selection_mode = not self.selection_mode
        
        if not self.selection_mode:
            self.selected_paths.clear()
        
        if self.on_mode_changed:
            self.on_mode_changed(self.selection_mode)
        if self.on_selection_changed:
            self.on_selection_changed(len(self.selected_paths))
    
    def toggle_project(self, path):
        """Adiciona/remove projeto da selecao sem rebuild de tela."""
        if not self.selection_mode:
            return
        
        if path in self.selected_paths:
            self.selected_paths.remove(path)
            is_selected = False
        else:
            self.selected_paths.add(path)
            is_selected = True
        
        # Atualiza visual cirúrgico do card (FIX-SELECTION-FLICKER)
        if self.on_card_toggled:
            self.on_card_toggled(path, is_selected)
        
        # Atualiza contador da barra
        if self.on_selection_changed:
            self.on_selection_changed(len(self.selected_paths))
    
    def select_all(self, paths):
        """Seleciona todos os projetos visíveis."""
        if not self.selection_mode:
            return
        
        self.selected_paths = set(paths)
        
        # Atualiza visual de todos os cards (FIX-SELECTION-FLICKER)
        if self.on_card_toggled:
            for p in paths:
                self.on_card_toggled(p, True)
        
        if self.on_selection_changed:
            self.on_selection_changed(len(self.selected_paths))
    
    def deselect_all(self):
        """Remove todas as selecoes."""
        # Atualiza visual antes de limpar o set (FIX-SELECTION-FLICKER)
        if self.on_card_toggled:
            for p in list(self.selected_paths):
                self.on_card_toggled(p, False)
        
        self.selected_paths.clear()
        
        if self.on_selection_changed:
            self.on_selection_changed(0)
    
    def remove_selected(self, parent_window):
        """Remove projetos selecionados do banco."""
        if not self.selected_paths:
            messagebox.showwarning(
                "Nenhum projeto selecionado",
                "Selecione ao menos um projeto para remover.",
                parent=parent_window
            )
            return
        
        count = len(self.selected_paths)
        confirm = messagebox.askyesno(
            "Confirmar remocao",
            f"Remover {count} projeto(s) selecionado(s)?\n\n"
            "Essa acao nao pode ser desfeita.",
            parent=parent_window
        )
        
        if not confirm:
            return
        
        for path in self.selected_paths:
            if path in self.database:
                del self.database[path]
            for collection_name in list(self.collections_manager.collections.keys()):
                if path in self.collections_manager.collections[collection_name]:
                    self.collections_manager.collections[collection_name].remove(path)
        
        # FIX-REMOVE: método correto é save_database(), não save()
        self.db_manager.save_database()
        self.collections_manager.save()
        
        removed_count = len(self.selected_paths)
        self.selected_paths.clear()
        self.selection_mode = False
        
        if self.on_mode_changed:
            self.on_mode_changed(False)
        if self.on_projects_removed:
            self.on_projects_removed(removed_count)
        if self.on_refresh_needed:
            self.on_refresh_needed()
