"""
core/protocols.py — Contratos formais de callback (VOLKOV-02)

Implementa o padrão Protocol (PEP 544) para tipar todos os callbacks
entre controllers e views. Elimina o padrão informal
'if self.on_xxx: self.on_xxx()' sem assinatura definida.

Uso:
    from core.protocols import RefreshCallback
    class MyController:
        def __init__(self) -> None:
            self.on_refresh: Optional[RefreshCallback] = None
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class RefreshCallback(Protocol):
    """Callback chamado quando a tela precisa ser atualizada."""
    def __call__(self) -> None: ...


@runtime_checkable
class ModeChangedCallback(Protocol):
    """Callback chamado quando o modo de seleção muda."""
    def __call__(self, is_active: bool) -> None: ...


@runtime_checkable
class ProjectsRemovedCallback(Protocol):
    """Callback chamado após remoção de projetos. Recebe a quantidade removida."""
    def __call__(self, count: int) -> None: ...


@runtime_checkable
class ProgressCallback(Protocol):
    """Callback de progresso para operações longas (importação, análise IA)."""
    def __call__(self, current: int, total: int, message: str) -> None: ...


@runtime_checkable
class DisplayUpdatedCallback(Protocol):
    """Callback disparado após atualização do painel de projetos."""
    def __call__(self, project_count: int) -> None: ...
