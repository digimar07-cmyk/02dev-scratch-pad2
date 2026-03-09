"""
ui/builders/cards_grid_builder.py — Construtor de grid de cards.

FASE-1.2B: Extração do método _build_cards_grid() do main_window.py
Redução: ~25 linhas

FIX-SELECTION-FLICKER: build() retorna {path: card_widget} para
atualização visual de seleção sem rebuild completo dos cards.

Responsabilidades:
- Construir grid de cards de projetos
- Calcular posição (row, col) de cada card
- Delegar renderização para build_card()
- Retornar registro de widgets para atualização cirurgião
"""
from config.card_layout import COLS
from ui.project_card import build_card


class CardsGridBuilder:
    """Construtor de grid de cards de projetos."""
    
    @staticmethod
    def build(parent, page_items, card_callbacks, start_row=2) -> dict:
        """
        Constrói grid de cards de projetos.
        
        Args:
            parent: Frame pai onde os cards serão inseridos
            page_items: Lista de tuplas (project_path, project_data)
            card_callbacks: Dicionário com callbacks para os cards
            start_row: Linha inicial do grid (padrão: 2)
        
        Returns:
            dict: {project_path: card_frame} para atualização visual cirurgião
        """
        card_registry = {}
        for i, (project_path, project_data) in enumerate(page_items):
            row = (i // COLS) + start_row
            col = i % COLS
            card_widget = build_card(
                parent, 
                project_path, 
                project_data, 
                card_callbacks, 
                row, 
                col
            )
            if card_widget is not None:
                card_registry[project_path] = card_widget
        return card_registry
