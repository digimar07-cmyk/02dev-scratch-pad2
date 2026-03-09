"""
tests/test_selection_controller.py — Testes do SelectionController

Cobre:
  - Ativar/desativar modo de seleção
  - Adicionar/remover projetos da seleção
  - select_all() e deselect_all()
  - remove_selected() com persistência real em disco
  - Disparo correto de callbacks
  - REGRESSION TEST: bug save() → save_database() (09/03/2026)

Referência DOCTORAL_APPROVAL_PLAN.md — TANAKA-04
"""
import pytest
import json
import os
import tempfile
from unittest.mock import MagicMock, patch
from core.database import DatabaseManager
from core.collections_manager import CollectionsManager
from ui.controllers.selection_controller import SelectionController


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_db_path():
    """Arquivo temporário para database. Cleanup automático."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    for f in [path, path + '.bak', path + '.tmp']:
        try:
            if os.path.exists(f):
                os.remove(f)
        except OSError:
            pass


@pytest.fixture
def tmp_collections_path():
    """Arquivo temporário para collections. Cleanup automático."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    for f in [path, path + '.bak', path + '.tmp']:
        try:
            if os.path.exists(f):
                os.remove(f)
        except OSError:
            pass


@pytest.fixture
def db_with_projects(tmp_db_path):
    """DatabaseManager com 3 projetos pré-carregados no disco."""
    data = {
        "/proj/alpha": {"name": "Alpha", "categories": ["Motion"], "tags": []},
        "/proj/beta":  {"name": "Beta",  "categories": ["Print"],  "tags": ["logo"]},
        "/proj/gamma": {"name": "Gamma", "categories": ["Motion"], "tags": []},
    }
    with open(tmp_db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    db = DatabaseManager(db_file=tmp_db_path)
    db.load_database()
    return db


@pytest.fixture
def collections_mgr(tmp_collections_path):
    """CollectionsManager isolado com arquivo temporário."""
    # Precisa de patch para evitar uso do COLLECTIONS_FILE global
    with patch('core.collections_manager.COLLECTIONS_FILE', tmp_collections_path):
        mgr = CollectionsManager()
    return mgr


@pytest.fixture
def ctrl(db_with_projects, collections_mgr):
    """SelectionController pronto para teste."""
    return SelectionController(
        database=db_with_projects.database,
        db_manager=db_with_projects,
        collections_manager=collections_mgr,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Testes de Modo de Seleção
# ─────────────────────────────────────────────────────────────────────────────

class TestSelectionMode:
    """Ativar e desativar modo de seleção."""

    def test_initial_state_is_off(self, ctrl):
        """Por padrão, modo de seleção deve estar desativado."""
        assert ctrl.selection_mode is False
        assert len(ctrl.selected_paths) == 0

    def test_toggle_mode_ativa(self, ctrl):
        """toggle_mode() deve ativar o modo."""
        ctrl.toggle_mode()
        assert ctrl.selection_mode is True

    def test_toggle_mode_desativa(self, ctrl):
        """Segundo toggle_mode() deve desativar o modo."""
        ctrl.toggle_mode()
        ctrl.toggle_mode()
        assert ctrl.selection_mode is False

    def test_desativar_limpa_selecao(self, ctrl):
        """Ao desativar, a seleção deve ser limpa."""
        ctrl.toggle_mode()
        ctrl.selected_paths.add("/proj/alpha")
        ctrl.toggle_mode()  # desativa
        assert len(ctrl.selected_paths) == 0

    def test_on_mode_changed_callback_ativacao(self, ctrl):
        """on_mode_changed deve ser chamado com True ao ativar."""
        cb = MagicMock()
        ctrl.on_mode_changed = cb
        ctrl.toggle_mode()
        cb.assert_called_once_with(True)

    def test_on_mode_changed_callback_desativacao(self, ctrl):
        """on_mode_changed deve ser chamado com False ao desativar."""
        cb = MagicMock()
        ctrl.toggle_mode()
        ctrl.on_mode_changed = cb
        ctrl.toggle_mode()
        cb.assert_called_once_with(False)


# ─────────────────────────────────────────────────────────────────────────────
# Testes de toggle_project()
# ─────────────────────────────────────────────────────────────────────────────

class TestToggleProject:
    """Adicionar e remover projetos da seleção."""

    def test_toggle_adiciona_projeto(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        assert "/proj/alpha" in ctrl.selected_paths

    def test_toggle_remove_projeto_ja_selecionado(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        ctrl.toggle_project("/proj/alpha")  # segundo toggle remove
        assert "/proj/alpha" not in ctrl.selected_paths

    def test_toggle_fora_do_modo_nao_faz_nada(self, ctrl):
        """toggle_project() sem modo ativo não deve adicionar nada."""
        ctrl.toggle_project("/proj/alpha")
        assert len(ctrl.selected_paths) == 0

    def test_on_card_toggled_callback_selecionado(self, ctrl):
        cb = MagicMock()
        ctrl.on_card_toggled = cb
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/beta")
        cb.assert_called_once_with("/proj/beta", True)

    def test_on_card_toggled_callback_desselecionado(self, ctrl):
        cb = MagicMock()
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/beta")
        ctrl.on_card_toggled = cb
        ctrl.toggle_project("/proj/beta")
        cb.assert_called_once_with("/proj/beta", False)

    def test_on_selection_changed_atualiza_contador(self, ctrl):
        cb = MagicMock()
        ctrl.on_selection_changed = cb
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        ctrl.toggle_project("/proj/beta")
        assert cb.call_count == 3  # 1 do toggle_mode + 2 do toggle_project


# ─────────────────────────────────────────────────────────────────────────────
# Testes de select_all() e deselect_all()
# ─────────────────────────────────────────────────────────────────────────────

class TestSelectAllDeselect:

    def test_select_all_seleciona_todos(self, ctrl):
        ctrl.toggle_mode()
        paths = list(ctrl.database.keys())
        ctrl.select_all(paths)
        assert ctrl.selected_paths == set(paths)

    def test_select_all_fora_do_modo_nao_faz_nada(self, ctrl):
        ctrl.select_all(["/proj/alpha", "/proj/beta"])
        assert len(ctrl.selected_paths) == 0

    def test_deselect_all_limpa_selecao(self, ctrl):
        ctrl.toggle_mode()
        ctrl.select_all(["/proj/alpha", "/proj/beta"])
        ctrl.deselect_all()
        assert len(ctrl.selected_paths) == 0

    def test_deselect_all_dispara_on_card_toggled_false(self, ctrl):
        cb = MagicMock()
        ctrl.toggle_mode()
        ctrl.select_all(["/proj/alpha", "/proj/beta"])
        ctrl.on_card_toggled = cb
        ctrl.deselect_all()
        # Cada card deve ter sido notificado como False
        called_paths = {call.args[0] for call in cb.call_args_list}
        assert "/proj/alpha" in called_paths
        assert "/proj/beta" in called_paths
        for call in cb.call_args_list:
            assert call.args[1] is False


# ─────────────────────────────────────────────────────────────────────────────
# Testes de remove_selected() — o mais crítico
# ─────────────────────────────────────────────────────────────────────────────

class TestRemoveSelected:

    def test_remove_apaga_da_memoria(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)
        assert "/proj/alpha" not in ctrl.database

    def test_remove_nao_toca_projeto_nao_selecionado(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)
        assert "/proj/beta" in ctrl.database
        assert "/proj/gamma" in ctrl.database

    def test_remove_multiplos_projetos(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        ctrl.toggle_project("/proj/beta")
        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)
        assert "/proj/alpha" not in ctrl.database
        assert "/proj/beta" not in ctrl.database
        assert "/proj/gamma" in ctrl.database

    def test_remove_limpa_selecao_apos_execucao(self, ctrl):
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)
        assert len(ctrl.selected_paths) == 0
        assert ctrl.selection_mode is False

    def test_remove_cancelado_nao_altera_nada(self, ctrl):
        original_count = len(ctrl.database)
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        with patch('tkinter.messagebox.askyesno', return_value=False):
            ctrl.remove_selected(parent_window=None)
        assert len(ctrl.database) == original_count

    def test_remove_sem_selecao_exibe_warning(self, ctrl):
        ctrl.toggle_mode()
        with patch('tkinter.messagebox.showwarning') as mock_warn:
            ctrl.remove_selected(parent_window=None)
            mock_warn.assert_called_once()

    def test_remove_dispara_on_projects_removed(self, ctrl):
        cb = MagicMock()
        ctrl.on_projects_removed = cb
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        ctrl.toggle_project("/proj/beta")
        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)
        cb.assert_called_once_with(2)

    def test_remove_dispara_on_refresh_needed(self, ctrl):
        cb = MagicMock()
        ctrl.on_refresh_needed = cb
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")
        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)
        cb.assert_called_once()

    # ── REGRESSION TEST ────────────────────────────────────────────────────
    # BUG DETECTADO: 09/03/2026
    # SINTOMA: Projetos removidos voltavam ao reiniciar o app.
    # CAUSA RAIZ: O método chamado era save() que não existe no DatabaseManager.
    #             O correto é save_database().
    # CORREÇÃO: selection_controller.py linha ~105: save_database() ✅
    # GARANTIA: Este teste FALHARIA com o código antigo (save() → AttributeError
    #           ou silêncio sem persistência).
    # ─────────────────────────────────────────────────────────────────────────
    def test_REGRESSION_remove_persiste_no_disco(self, ctrl, db_with_projects, tmp_db_path):
        """
        REGRESSION — BUG 09/03/2026: save() → save_database()

        Garante que projetos removidos NÃO voltam após reiniciar o app.
        Recria o DatabaseManager do zero (simulando reinicialização)
        e verifica que o projeto removido está ausente do disco.
        """
        ctrl.toggle_mode()
        ctrl.toggle_project("/proj/alpha")

        with patch('tkinter.messagebox.askyesno', return_value=True):
            ctrl.remove_selected(parent_window=None)

        # Simula reinicialização: novo DatabaseManager lendo o mesmo arquivo
        db_reloaded = DatabaseManager(db_file=tmp_db_path)
        db_reloaded.load_database()

        assert "/proj/alpha" not in db_reloaded.database, (
            "REGRESSION BUG 09/03/2026: Projeto removido voltou após reload! "
            "Verificar se save_database() está sendo chamado corretamente."
        )
        assert "/proj/beta" in db_reloaded.database
        assert "/proj/gamma" in db_reloaded.database
        assert len(db_reloaded.database) == 2
