"""
ui/components/chips_bar.py — Barra de chips de filtros ativos.

FASE 7D.1: Extrai lógica de chips do main_window.py
Redução estimada: -45 linhas no main_window.py
"""

import tkinter as tk

from ui.theme import ACCENT_BLUE, BG_PRIMARY, FG_PRIMARY


class ChipsBar:
    """
    Component para exibir chips de filtros ativos.

    Responsabilidades:
    - Renderizar chips com base em filtros ativos
    - Botão "X" para remover filtro individual
    - Botão "Limpar tudo" para remover todos os filtros
    """

    def __init__(self, parent, bg_color=BG_PRIMARY):
        self.parent = parent
        self.bg_color = bg_color

        # Frame principal
        self.frame = tk.Frame(parent, bg=bg_color, height=50)
        self.frame.pack_propagate(False)

        # Container interno para chips
        self.container = tk.Frame(self.frame, bg=bg_color)
        self.container.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        # Callbacks
        self.on_chip_removed = None  # callback(filter_type: str)
        self.on_clear_all = None  # callback()

    def update(self, active_filters):
        """
        Atualiza chips com base nos filtros ativos.

        Args:
            active_filters: Dict com filtros ativos
                {
                    "type": str,
                    "origin": str,
                    "search": str,
                    "category": str,
                    "favorite": bool,
                    "done": bool,
                    "collection": str,
                }
        """
        # Limpar chips existentes
        for widget in self.container.winfo_children():
            widget.destroy()

        # Contador de filtros
        count = 0

        # Chip de tipo
        if active_filters.get("type"):
            self._create_chip(f"Tipo: {active_filters['type']}", "type")
            count += 1

        # Chip de origem
        if active_filters.get("origin"):
            self._create_chip(f"Origem: {active_filters['origin']}", "origin")
            count += 1

        # Chip de busca
        if active_filters.get("search"):
            search_text = active_filters["search"]
            if len(search_text) > 30:
                search_text = search_text[:27] + "..."
            self._create_chip(f'🔍 "{search_text}"', "search")
            count += 1

        # Chip de categoria
        if active_filters.get("category"):
            self._create_chip(f"Categoria: {active_filters['category']}", "category")
            count += 1

        # Chip de favoritos
        if active_filters.get("favorite"):
            self._create_chip("⭐ Favoritos", "favorite")
            count += 1

        # Chip de concluídos
        if active_filters.get("done"):
            self._create_chip("✓ Concluídos", "done")
            count += 1

        # Chip de coleção
        if active_filters.get("collection"):
            col_name = active_filters["collection"]
            if len(col_name) > 20:
                col_name = col_name[:17] + "..."
            self._create_chip(f"📁 {col_name}", "collection")
            count += 1

        # Botão "Limpar tudo" se houver filtros
        if count > 1:
            clear_btn = tk.Button(
                self.container,
                text="✕ Limpar tudo",
                bg="#3A3A4E",
                fg=FG_PRIMARY,
                font=("Segoe UI", 9),
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=4,
                command=self._on_clear_all_clicked,
            )
            clear_btn.pack(side="left", padx=4)

        # Mostrar/ocultar frame baseado na quantidade de filtros
        if count > 0:
            self.show()
        else:
            self.hide()

    def _create_chip(self, text, filter_type):
        """Cria um chip individual."""
        chip_frame = tk.Frame(self.container, bg="#2A2A3E", relief="flat")
        chip_frame.pack(side="left", padx=4)

        label = tk.Label(
            chip_frame,
            text=text,
            bg="#2A2A3E",
            fg=FG_PRIMARY,
            font=("Segoe UI", 9),
            padx=8,
            pady=4,
        )
        label.pack(side="left")

        remove_btn = tk.Button(
            chip_frame,
            text="✕",
            bg="#2A2A3E",
            fg="#888888",
            font=("Segoe UI", 8),
            relief="flat",
            cursor="hand2",
            padx=4,
            pady=2,
            command=lambda: self._on_chip_removed(filter_type),
        )
        remove_btn.pack(side="left", padx=(0, 4))

        def on_enter(_event):
            remove_btn.config(fg="#FF4444")

        def on_leave(_event):
            remove_btn.config(fg="#888888")

        remove_btn.bind("<Enter>", on_enter)
        remove_btn.bind("<Leave>", on_leave)

    def _on_chip_removed(self, filter_type):
        """Callback quando chip é removido."""
        if self.on_chip_removed:
            self.on_chip_removed(filter_type)

    def _on_clear_all_clicked(self):
        """Callback quando 'Limpar tudo' é clicado."""
        if self.on_clear_all:
            self.on_clear_all()

    def show(self):
        """Mostra a barra de chips."""
        self.frame.pack(side="top", fill="x", padx=10, pady=(10, 0))

    def hide(self):
        """Esconde a barra de chips."""
        self.frame.pack_forget()

    def is_visible(self):
        """Verifica se está visível."""
        return self.frame.winfo_ismapped()