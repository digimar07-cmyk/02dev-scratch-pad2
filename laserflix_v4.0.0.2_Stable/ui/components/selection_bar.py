"""
ui/components/selection_bar.py — Barra de ferramentas para modo seleção.

FASE 7D.2: Extrai construção de selection bar do main_window.py
Redução estimada: -45 linhas no main_window.py
"""
import tkinter as tk
from ui.theme import FG_PRIMARY, FG_SECONDARY


class SelectionBar:
    """
    Component para barra de ferramentas do modo seleção.
    
    Responsabilidades:
    - Exibir contador de selecionados
    - Botões: Selecionar tudo, Deselecionar tudo, Remover, Cancelar
    """
    
    def __init__(self, parent):
        self.parent = parent
        
        # Frame principal
        self.frame = tk.Frame(parent, bg="#1A1A00", height=48)
        self.frame.pack_propagate(False)
        
        # Contador
        self.count_label = tk.Label(
            self.frame,
            text="0 selecionado(s)",
            bg="#1A1A00",
            fg=FG_PRIMARY,
            font=("Segoe UI", 10, "bold")
        )
        self.count_label.pack(side="left", padx=15)
        
        # Container de botões
        btn_container = tk.Frame(self.frame, bg="#1A1A00")
        btn_container.pack(side="right", padx=10)
        
        # Botão Selecionar tudo
        self.select_all_btn = tk.Button(
            btn_container,
            text="✓ Selecionar tudo",
            bg="#2A2A3E",
            fg=FG_PRIMARY,
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )
        self.select_all_btn.pack(side="left", padx=4)
        
        # Botão Deselecionar tudo
        self.deselect_all_btn = tk.Button(
            btn_container,
            text="✕ Deselecionar tudo",
            bg="#2A2A3E",
            fg=FG_PRIMARY,
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )
        self.deselect_all_btn.pack(side="left", padx=4)
        
        # Botão Remover selecionados
        self.remove_btn = tk.Button(
            btn_container,
            text="🗑️ Remover selecionados",
            bg="#AA3333",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )
        self.remove_btn.pack(side="left", padx=4)
        
        # Botão Cancelar
        self.cancel_btn = tk.Button(
            btn_container,
            text="Cancelar",
            bg="#3A3A4E",
            fg=FG_SECONDARY,
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )
        self.cancel_btn.pack(side="left", padx=4)
        
        # Callbacks
        self.on_select_all = None
        self.on_deselect_all = None
        self.on_remove_selected = None
        self.on_cancel = None
        
        # Conectar comandos
        self.select_all_btn.config(command=self._on_select_all_clicked)
        self.deselect_all_btn.config(command=self._on_deselect_all_clicked)
        self.remove_btn.config(command=self._on_remove_clicked)
        self.cancel_btn.config(command=self._on_cancel_clicked)
        
        # Hover effects
        self._setup_hover_effects()
    
    def _setup_hover_effects(self):
        """Configura efeitos de hover nos botões."""
        for btn, hover_bg in [
            (self.select_all_btn, "#3A3A4E"),
            (self.deselect_all_btn, "#3A3A4E"),
            (self.remove_btn, "#CC4444"),
            (self.cancel_btn, "#4A4A5E")
        ]:
            original_bg = btn.cget("bg")
            btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, o=original_bg: b.config(bg=o))
    
    def update_count(self, count):
        """Atualiza contador de selecionados."""
        self.count_label.config(text=f"{count} selecionado(s)")
        
        # Habilitar/desabilitar botões baseado no count
        state = "normal" if count > 0 else "disabled"
        self.deselect_all_btn.config(state=state)
        self.remove_btn.config(state=state)
    
    def show(self):
        """Mostra a barra de seleção."""
        self.frame.pack(side="top", fill="x", after=self.parent.winfo_children()[0])
    
    def hide(self):
        """Esconde a barra de seleção."""
        self.frame.pack_forget()
    
    def is_visible(self):
        """Verifica se está visível."""
        return self.frame.winfo_ismapped()
    
    # Callbacks internos
    def _on_select_all_clicked(self):
        if self.on_select_all:
            self.on_select_all()
    
    def _on_deselect_all_clicked(self):
        if self.on_deselect_all:
            self.on_deselect_all()
    
    def _on_remove_clicked(self):
        if self.on_remove_selected:
            self.on_remove_selected()
    
    def _on_cancel_clicked(self):
        if self.on_cancel:
            self.on_cancel()
