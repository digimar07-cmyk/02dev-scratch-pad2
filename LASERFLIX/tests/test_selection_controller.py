"""
test_selection_controller.py — Testes do SelectionController

Cobre:
  - Ativar/desativar modo seleção
  - Adicionar/remover projetos da seleção
  - Select all / Deselect all
  - Remoção múltipla de projetos
  - Callbacks de mudança de estado
"""
import pytest
from unittest.mock import Mock, MagicMock
from ui.controllers.selection_controller import SelectionController


@pytest.fixture
def mock_database():
    """Mock de database com 3 projetos."""
    return {
        "/project1": {"name": "Project 1"},
        "/project2": {"name": "Project 2"},
        "/project3": {"name": "Project 3"},
    }


@pytest.fixture
def mock_db_manager():
    """Mock de DatabaseManager."""
    manager = Mock()
    manager.save_database = Mock()
    return manager


@pytest.fixture
def mock_collections_manager():
    """Mock de CollectionsManager."""
    manager = Mock()
    manager.collections = {
        "Collection A": ["/project1", "/project2"],
        "Collection B": ["/project3"],
    }
    manager.save = Mock()
    return manager


@pytest.fixture
def controller(mock_database, mock_db_manager, mock_collections_manager):
    """Controller configurado para testes."""
    return SelectionController(
        database=mock_database,
        db_manager=mock_db_manager,
        collections_manager=mock_collections_manager,
    )


class TestSelectionMode:
    """Testes de ativação/desativação do modo seleção."""
    
    def test_toggle_mode_activates(self, controller):
        """
        SMOKE TEST: toggle_mode() deve ativar modo seleção.
        """
        assert controller.selection_mode is False
        
        controller.toggle_mode()
        
        assert controller.selection_mode is True
    
    def test_toggle_mode_deactivates_and_clears_selection(self, controller):
        """
        COMPORTAMENTO: Desativar modo deve limpar seleção.
        """
        controller.selection_mode = True
        controller.selected_paths = {"/project1", "/project2"}
        
        controller.toggle_mode()
        
        assert controller.selection_mode is False
        assert len(controller.selected_paths) == 0
    
    def test_toggle_mode_calls_callback(self, controller):
        """
        CALLBACK: on_mode_changed deve ser chamado ao mudar modo.
        """
        callback = Mock()
        controller.on_mode_changed = callback
        
        controller.toggle_mode()
        
        callback.assert_called_once_with(True)


class TestProjectSelection:
    """Testes de seleção individual de projetos."""
    
    def test_toggle_project_adds_to_selection(self, controller):
        """
        SMOKE TEST: toggle_project() deve adicionar projeto à seleção.
        """
        controller.selection_mode = True
        
        controller.toggle_project("/project1")
        
        assert "/project1" in controller.selected_paths
        assert len(controller.selected_paths) == 1
    
    def test_toggle_project_removes_from_selection(self, controller):
        """
        COMPORTAMENTO: toggle no projeto já selecionado deve remover.
        """
        controller.selection_mode = True
        controller.selected_paths = {"/project1"}
        
        controller.toggle_project("/project1")
        
        assert "/project1" not in controller.selected_paths
        assert len(controller.selected_paths) == 0
    
    def test_toggle_project_calls_card_toggled_callback(self, controller):
        """
        CALLBACK: on_card_toggled deve ser chamado ao selecionar.
        """
        callback = Mock()
        controller.on_card_toggled = callback
        controller.selection_mode = True
        
        controller.toggle_project("/project1")
        
        callback.assert_called_once_with("/project1", True)
    
    def test_toggle_project_calls_selection_changed_callback(self, controller):
        """
        CALLBACK: on_selection_changed deve ser chamado com contador.
        """
        callback = Mock()
        controller.on_selection_changed = callback
        controller.selection_mode = True
        
        controller.toggle_project("/project1")
        
        callback.assert_called_once_with(1)
    
    def test_toggle_project_ignores_when_mode_inactive(self, controller):
        """
        EDGE CASE: toggle quando modo está desativado não faz nada.
        """
        controller.selection_mode = False
        
        controller.toggle_project("/project1")
        
        assert len(controller.selected_paths) == 0


class TestBulkSelection:
    """Testes de seleção/desseleção em massa."""
    
    def test_select_all(self, controller):
        """
        OPERAÇÃO: select_all() deve selecionar todos os projetos passados.
        """
        controller.selection_mode = True
        visible_paths = ["/project1", "/project2", "/project3"]
        
        controller.select_all(visible_paths)
        
        assert len(controller.selected_paths) == 3
        assert "/project1" in controller.selected_paths
        assert "/project2" in controller.selected_paths
        assert "/project3" in controller.selected_paths
    
    def test_select_all_calls_callbacks(self, controller):
        """
        CALLBACK: select_all deve chamar on_card_toggled para cada projeto.
        """
        card_callback = Mock()
        selection_callback = Mock()
        controller.on_card_toggled = card_callback
        controller.on_selection_changed = selection_callback
        controller.selection_mode = True
        
        controller.select_all(["/project1", "/project2"])
        
        assert card_callback.call_count == 2
        selection_callback.assert_called_once_with(2)
    
    def test_deselect_all(self, controller):
        """
        OPERAÇÃO: deselect_all() deve limpar seleção.
        """
        controller.selection_mode = True
        controller.selected_paths = {"/project1", "/project2"}
        
        controller.deselect_all()
        
        assert len(controller.selected_paths) == 0
    
    def test_deselect_all_calls_callbacks(self, controller):
        """
        CALLBACK: deselect_all deve chamar on_card_toggled(path, False) para cada.
        """
        card_callback = Mock()
        selection_callback = Mock()
        controller.on_card_toggled = card_callback
        controller.on_selection_changed = selection_callback
        controller.selection_mode = True
        controller.selected_paths = {"/project1", "/project2"}
        
        controller.deselect_all()
        
        assert card_callback.call_count == 2
        # Verificar que foi chamado com False para cada projeto
        calls = card_callback.call_args_list
        for call in calls:
            assert call[0][1] is False  # segundo argumento (is_selected) deve ser False
        
        selection_callback.assert_called_once_with(0)


class TestRemoveSelected:
    """Testes de remoção múltipla de projetos."""
    
    def test_remove_selected_deletes_from_database(self, controller, mock_database, mock_db_manager):
        """
        OPERAÇÃO: remove_selected() deve deletar projetos do database.
        """
        controller.selection_mode = True
        controller.selected_paths = {"/project1", "/project2"}
        
        # Mock do messagebox.askyesno para confirmar remoção
        import ui.controllers.selection_controller as sc_module
        original_messagebox = sc_module.messagebox
        sc_module.messagebox = Mock()
        sc_module.messagebox.askyesno = Mock(return_value=True)
        
        try:
            controller.remove_selected(parent_window=None)
            
            # Verificar que projetos foram removidos
            assert "/project1" not in mock_database
            assert "/project2" not in mock_database
            assert "/project3" in mock_database  # não selecionado, deve permanecer
            
            # Verificar que save foi chamado
            mock_db_manager.save_database.assert_called_once()
        
        finally:
            sc_module.messagebox = original_messagebox
    
    def test_remove_selected_cleans_collections(self, controller, mock_collections_manager):
        """
        INTEGRAÇÃO: remove_selected() deve limpar projetos das coleções.
        """
        controller.selection_mode = True
        controller.selected_paths = {"/project1"}
        
        # Mock do messagebox
        import ui.controllers.selection_controller as sc_module
        original_messagebox = sc_module.messagebox
        sc_module.messagebox = Mock()
        sc_module.messagebox.askyesno = Mock(return_value=True)
        
        try:
            controller.remove_selected(parent_window=None)
            
            # Verificar que projeto foi removido da coleção
            assert "/project1" not in mock_collections_manager.collections["Collection A"]
            
            # Verificar que save foi chamado
            mock_collections_manager.save.assert_called_once()
        
        finally:
            sc_module.messagebox = original_messagebox
    
    def test_remove_selected_calls_callbacks(self, controller):
        """
        CALLBACK: remove_selected() deve chamar callbacks de refresh.
        """
        mode_callback = Mock()
        removed_callback = Mock()
        refresh_callback = Mock()
        controller.on_mode_changed = mode_callback
        controller.on_projects_removed = removed_callback
        controller.on_refresh_needed = refresh_callback
        controller.selection_mode = True
        controller.selected_paths = {"/project1", "/project2"}
        
        # Mock do messagebox
        import ui.controllers.selection_controller as sc_module
        original_messagebox = sc_module.messagebox
        sc_module.messagebox = Mock()
        sc_module.messagebox.askyesno = Mock(return_value=True)
        
        try:
            controller.remove_selected(parent_window=None)
            
            mode_callback.assert_called_once_with(False)  # modo desativado após remoção
            removed_callback.assert_called_once_with(2)   # 2 projetos removidos
            refresh_callback.assert_called_once()         # refresh da UI
        
        finally:
            sc_module.messagebox = original_messagebox
    
    def test_remove_selected_shows_warning_when_empty(self, controller):
        """
        EDGE CASE: remove_selected() sem seleção deve mostrar warning.
        """
        controller.selected_paths = set()
        
        # Mock do messagebox
        import ui.controllers.selection_controller as sc_module
        original_messagebox = sc_module.messagebox
        sc_module.messagebox = Mock()
        sc_module.messagebox.showwarning = Mock()
        
        try:
            controller.remove_selected(parent_window=None)
            
            sc_module.messagebox.showwarning.assert_called_once()
        
        finally:
            sc_module.messagebox = original_messagebox
