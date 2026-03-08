# -*- coding: utf-8 -*-
"""
Gerencia toggles (favorito, done, good, bad).

FASE-2A: Métodos consolidados com base genérica.
- _toggle_field() centraliza lógica comum
- Métodos específicos viram wrappers leves
- Redução: -30 linhas de código duplicado
"""
from config.ui_constants import ACCENT_GOLD, FG_TERTIARY


class ToggleManager:
    def __init__(self, database, db_manager):
        self.database = database
        self.db_manager = db_manager
        self.on_invalidate_cache = None
    
    def _toggle_field(self, path: str, field: str, btn=None, btn_updater=None, exclusive_field=None):
        """
        Método genérico de toggle (FASE-2A).
        
        Args:
            path: Caminho do projeto
            field: Campo a ser toggleado ("favorite", "done", "good", "bad")
            btn: Botão Tkinter (opcional)
            btn_updater: Função (btn, new_value) -> None que atualiza visual do botão
            exclusive_field: Campo exclusivo a desmarcar (ex: "bad" ao marcar "good")
        """
        if path not in self.database:
            return
        
        # Toggle valor
        new_value = not self.database[path].get(field, False)
        self.database[path][field] = new_value
        
        # Exclusividade (good/bad)
        if new_value and exclusive_field:
            self.database[path][exclusive_field] = False
        
        # Salvar e invalidar cache
        self.db_manager.save_database()
        if self.on_invalidate_cache:
            self.on_invalidate_cache()
        
        # Atualizar visual do botão
        if btn and btn_updater:
            btn_updater(btn, new_value)
    
    # =========================================================================
    # MÉTODOS PÚBLICOS (wrappers específicos)
    # =========================================================================
    
    def toggle_favorite(self, path: str, btn=None):
        """Toggle favorito (★/☆)."""
        def update_btn(b, is_active):
            b.config(
                text="⭐" if is_active else "☆",
                fg=ACCENT_GOLD if is_active else FG_TERTIARY
            )
        
        self._toggle_field(path, "favorite", btn, update_btn)
    
    def toggle_done(self, path: str, btn=None):
        """Toggle concluído (✓/○)."""
        def update_btn(b, is_active):
            b.config(
                text="✓" if is_active else "○",
                fg="#00FF00" if is_active else FG_TERTIARY
            )
        
        self._toggle_field(path, "done", btn, update_btn)
    
    def toggle_good(self, path: str, btn=None):
        """Toggle qualidade boa (👍). Exclusivo com 'bad'."""
        def update_btn(b, is_active):
            b.config(fg="#00FF00" if is_active else FG_TERTIARY)
        
        self._toggle_field(path, "good", btn, update_btn, exclusive_field="bad")
    
    def toggle_bad(self, path: str, btn=None):
        """Toggle qualidade ruim (👎). Exclusivo com 'good'."""
        def update_btn(b, is_active):
            b.config(fg="#FF0000" if is_active else FG_TERTIARY)
        
        self._toggle_field(path, "bad", btn, update_btn, exclusive_field="good")
