"""
test_selection_controller.py — Testes agressivos para encontrar bugs reais.

Estratégia: condições de corrida, callbacks None, remoção com dados inválidos,
bordas que o usuário real pode causar.
"""
import pytest
from unittest.mock import MagicMock, patch
from core.database import DatabaseManager
from core.collections_manager import CollectionsManager
from ui.controllers.selection_controller import SelectionController


# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def setup(tmp_path):
    db_file = str(tmp_path / "database.json")
    cfg_file = str(tmp_path / "config.json")
    col_file = str(tmp_path / "collections.json")
    db_manager = DatabaseManager(db_file=db_file, config_file=cfg_file)
    cm = CollectionsManager(file_path=col_file)
    database = db_manager.database
    ctrl = SelectionController(database, db_manager, cm)
    return ctrl, db_manager, cm, database


# ══════════════════════════════════════════════════════════════
# CALLBACKS — o que acontece quando callbacks não estão conectados
# ══════════════════════════════════════════════════════════════

class TestCallbacksNaoConectados:
    """Todos os callbacks são opcionais. Nada pode travar quando são None."""

    def test_toggle_mode_sem_callbacks_nao_trava(self, setup):
        ctrl, *_ = setup
        # Todos callbacks são None por padrão
        try:
            ctrl.toggle_mode()
            ctrl.toggle_mode()
        except Exception as e:
            pytest.fail(f"BUG: toggle_mode() sem callbacks lança exceção: {e}")

    def test_toggle_project_sem_callbacks_nao_trava(self, setup):
        ctrl, *_ = setup
        ctrl.toggle_mode()  # ativa modo
        try:
            ctrl.toggle_project("/path/a")
        except Exception as e:
            pytest.fail(f"BUG: toggle_project() sem callbacks lança exceção: {e}")

    def test_select_all_sem_callbacks_nao_trava(self, setup):
        ctrl, *_ = setup
        ctrl.toggle_mode()
        try:
            ctrl.select_all(["/path/a", "/path/b", "/path/c"])
        except Exception as e:
            pytest.fail(f"BUG: select_all() sem callbacks lança exceção: {e}")

    def test_deselect_all_sem_callbacks_nao_trava(self, setup):
        ctrl, *_ = setup
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/path/a", "/path/b"}
        try:
            ctrl.deselect_all()
        except Exception as e:
            pytest.fail(f"BUG: deselect_all() sem callbacks lança exceção: {e}")


# ══════════════════════════════════════════════════════════════
# REMOÇÃO — operação mais crítica do app
# ══════════════════════════════════════════════════════════════

class TestRemocaoCritica:

    def test_remove_projeto_que_nao_existe_no_database(self, setup):
        """Remover path que não está no database não pode lançar KeyError."""
        ctrl, db_manager, cm, database = setup
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/path/fantasma"}  # não existe no banco
        parent = MagicMock()
        with patch("ui.controllers.selection_controller.messagebox") as mock_mb:
            mock_mb.askyesno.return_value = True
            try:
                ctrl.remove_selected(parent)
            except KeyError as e:
                pytest.fail(f"BUG: remove_selected com path inexistente lança KeyError: {e}")

    def test_remove_limpa_colecoes_do_projeto_removido(self, setup):
        """Ao remover projeto, ele deve ser removido das coleções também."""
        ctrl, db_manager, cm, database = setup
        database["/path/a"] = {"name": "A"}
        cm.create_collection("Favoritos")
        cm.collections["Favoritos"].append("/path/a")
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/path/a"}
        parent = MagicMock()
        with patch("ui.controllers.selection_controller.messagebox") as mock_mb:
            mock_mb.askyesno.return_value = True
            ctrl.remove_selected(parent)
        assert "/path/a" not in cm.get_projects("Favoritos"), (
            "BUG: projeto removido do database mas continua na coleção. "
            "Coleção fica com referência fantasma."
        )

    def test_remove_nao_persiste_sem_confirmacao(self, setup):
        """Se usuário cancelar a confirmação, NADA deve ser alterado no banco."""
        ctrl, db_manager, cm, database = setup
        database["/path/a"] = {"name": "A"}
        database["/path/b"] = {"name": "B"}
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/path/a", "/path/b"}
        parent = MagicMock()
        with patch("ui.controllers.selection_controller.messagebox") as mock_mb:
            mock_mb.askyesno.return_value = False  # usuário cancelou
            ctrl.remove_selected(parent)
        assert "/path/a" in database, "BUG: projeto removido mesmo com confirmação cancelada"
        assert "/path/b" in database, "BUG: projeto removido mesmo com confirmação cancelada"
        assert db_manager.project_count() == 2

    def test_remove_desativa_modo_selecao_apos_remocao(self, setup):
        """Após remoção confirmada, modo seleção deve ser desativado."""
        ctrl, db_manager, cm, database = setup
        database["/path/a"] = {"name": "A"}
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/path/a"}
        parent = MagicMock()
        with patch("ui.controllers.selection_controller.messagebox") as mock_mb:
            mock_mb.askyesno.return_value = True
            ctrl.remove_selected(parent)
        assert ctrl.selection_mode is False, (
            "BUG: modo seleção continua ativo após remoção. "
            "UI fica em estado inconsistente."
        )
        assert len(ctrl.selected_paths) == 0

    def test_remove_com_selected_paths_modificado_durante_iteracao(self, setup):
        """Modificar selected_paths durante iteração não pode causar RuntimeError."""
        ctrl, db_manager, cm, database = setup
        for i in range(10):
            database[f"/path/{i}"] = {"name": f"P{i}"}
        ctrl.toggle_mode()
        ctrl.select_all([f"/path/{i}" for i in range(10)])
        parent = MagicMock()
        with patch("ui.controllers.selection_controller.messagebox") as mock_mb:
            mock_mb.askyesno.return_value = True
            try:
                ctrl.remove_selected(parent)
            except RuntimeError as e:
                pytest.fail(f"BUG: iteração sobre set modificado causa RuntimeError: {e}")
        assert len(database) == 0


# ══════════════════════════════════════════════════════════════
# ESTADO INCONSISTENTE — o app pode entrar em estado impossível?
# ══════════════════════════════════════════════════════════════

class TestEstadoInconsistente:

    def test_selected_paths_fora_do_modo_selecao(self, setup):
        """selected_paths com itens enquanto selection_mode=False é estado inválido."""
        ctrl, *_ = setup
        # Força estado inválido manualmente (como poderia acontecer por bug)
        ctrl.selection_mode = False
        ctrl.selected_paths = {"/path/a", "/path/b"}
        # toggle_mode deve limpar selected_paths ao ativar e desativar
        ctrl.toggle_mode()  # ativa
        ctrl.toggle_mode()  # desativa
        assert len(ctrl.selected_paths) == 0, (
            "BUG: selected_paths não foi limpo ao desativar modo seleção. "
            "Itens de uma sessão anterior persistem na próxima."
        )

    def test_toggle_project_com_path_none(self, setup):
        """toggle_project(None) não pode travar com TypeError."""
        ctrl, *_ = setup
        ctrl.toggle_mode()
        try:
            ctrl.toggle_project(None)
        except TypeError as e:
            pytest.fail(f"BUG: toggle_project(None) lança TypeError: {e}")

    def test_select_all_com_lista_vazia(self, setup):
        """select_all([]) deve resultar em 0 selecionados, não manter estado anterior."""
        ctrl, *_ = setup
        ctrl.toggle_mode()
        ctrl.selected_paths = {"/path/anterior"}  # estado anterior
        ctrl.select_all([])
        assert len(ctrl.selected_paths) == 0, (
            "BUG: select_all([]) não limpou selected_paths. "
            "Itens de seleção anterior persistem."
        )

    def test_select_all_com_paths_duplicados(self, setup):
        """select_all com lista que tem duplicatas não deve contar duplicado."""
        ctrl, *_ = setup
        ctrl.toggle_mode()
        ctrl.select_all(["/path/a", "/path/a", "/path/a"])
        assert len(ctrl.selected_paths) == 1, (
            f"BUG: select_all com duplicatas gerou {len(ctrl.selected_paths)} selecionados. "
            "Contador na UI vai mostrar número errado."
        )
