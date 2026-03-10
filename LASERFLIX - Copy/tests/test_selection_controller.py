"""
tests/test_selection_controller.py — TANAKA-04

Cobre: SelectionController (toggle_mode, toggle_project, select_all,
       deselect_all, remove_selected)

REGRESSION TEST (bug 09/03/2026):
    test_remove_persiste_em_disco — garante que save_database() é chamado
    após remoção. Antes do fix, o método era save() (inexistente).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ui.controllers.selection_controller import SelectionController
from core.database import DatabaseManager


@pytest.fixture
def ctrl(tmp_db_with_data, tmp_collections):
    c = SelectionController(
        database=tmp_db_with_data.database,
        db_manager=tmp_db_with_data,
        collections_manager=tmp_collections,
    )
    return c


# ── Modo Seleção ───────────────────────────────────────────────────────

class TestToggleMode:
    def test_ativa_modo_selecao(self, ctrl):
        ctrl.toggle_mode()
        assert ctrl.selection_mode is True

    def test_desativa_modo_selecao(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_mode()
        assert ctrl.selection_mode is False

    def test_desativar_limpa_selecao(self, ctrl):
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/alpha"}
        ctrl.toggle_mode()
        assert len(ctrl.selected_paths) == 0

    def test_callback_on_mode_changed_chamado(self, ctrl):
        cb = MagicMock()
        ctrl.on_mode_changed = cb
        ctrl.toggle_mode()
        cb.assert_called_once_with(True)


# ── Toggle/Select ─────────────────────────────────────────────────────

class TestToggleProject:
    def test_adiciona_projeto_na_selecao(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        assert "/proj/alpha" in ctrl.selected_paths

    def test_remove_projeto_ja_selecionado(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        ctrl.toggle_project("/proj/alpha")
        assert "/proj/alpha" not in ctrl.selected_paths

    def test_toggle_fora_do_modo_nao_faz_nada(self, ctrl):
        ctrl.toggle_project("/proj/alpha")
        assert "/proj/alpha" not in ctrl.selected_paths

    def test_select_all(self, ctrl):
        ctrl.toggle_mode()
        paths = ["/proj/alpha", "/proj/beta", "/proj/gamma"]
        ctrl.select_all(paths)
        assert ctrl.selected_paths == set(paths)

    def test_deselect_all(self, ctrl):
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/alpha", "/proj/beta"}
        ctrl.deselect_all()
        assert len(ctrl.selected_paths) == 0


# ── Remoção ────────────────────────────────────────────────────────────

class TestRemoveSelected:
    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showwarning")
    def test_remove_da_memoria(self, mock_warn, mock_confirm, ctrl):
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/beta"}
        ctrl.remove_selected(parent_window=None)
        assert "/proj/beta" not in ctrl.database

    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showwarning")
    def test_remove_persiste_em_disco(self, mock_warn, mock_confirm, tmp_db_with_data, tmp_collections, tmp_path):
        """
        REGRESSION TEST — bug 09/03/2026
        save() não existia. Após remoção, reiniciar o app trazia projetos de volta.
        Este teste garante que save_database() é chamado e o disco é atualizado.
        """
        ctrl = SelectionController(
            database=tmp_db_with_data.database,
            db_manager=tmp_db_with_data,
            collections_manager=tmp_collections,
        )
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/alpha"}
        ctrl.remove_selected(parent_window=None)

        db2 = DatabaseManager(db_file=str(tmp_path / "test_db.json"))
        db2.load_database()
        assert "/proj/alpha" not in db2.database

    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showwarning")
    def test_remove_nao_toca_outros_projetos(self, mock_warn, mock_confirm, ctrl):
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/alpha"}
        ctrl.remove_selected(parent_window=None)
        assert "/proj/beta" in ctrl.database
        assert "/proj/gamma" in ctrl.database

    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showwarning")
    def test_remove_chama_callback_projects_removed(self, mock_warn, mock_confirm, ctrl):
        cb = MagicMock()
        ctrl.on_projects_removed = cb
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/alpha", "/proj/beta"}
        ctrl.remove_selected(parent_window=None)
        cb.assert_called_once_with(2)

    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showwarning")
    def test_remove_chama_callback_refresh(self, mock_warn, mock_confirm, ctrl):
        cb = MagicMock()
        ctrl.on_refresh_needed = cb
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/gamma"}
        ctrl.remove_selected(parent_window=None)
        cb.assert_called_once()

    @patch("tkinter.messagebox.showwarning")
    def test_remove_selecao_vazia_nao_remove_nada(self, mock_warn, ctrl):
        original = len(ctrl.database)
        ctrl.toggle_mode()
        ctrl.selected_paths = set()
        ctrl.remove_selected(parent_window=None)
        assert len(ctrl.database) == original

    @patch("tkinter.messagebox.askyesno", return_value=False)
    @patch("tkinter.messagebox.showwarning")
    def test_cancel_confirmacao_nao_remove(self, mock_warn, mock_confirm, ctrl):
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/proj/alpha"}
        ctrl.remove_selected(parent_window=None)
        assert "/proj/alpha" in ctrl.database
