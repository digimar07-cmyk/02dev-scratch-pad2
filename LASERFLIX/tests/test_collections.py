"""
test_collections.py — Testes do CollectionsManager

Cobre:
  - CRUD de coleções (criar, renomear, deletar)
  - Adição/remoção de projetos
  - Limpeza de referências órfãs
  - Edge cases (coleção inexistente, duplicatas)
"""
import pytest
import os
import tempfile
from core.collections_manager import CollectionsManager


@pytest.fixture
def temp_collections_file():
    """
    Cria arquivo temporário para testar CollectionsManager.
    """
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    # Sobrescreve o caminho padrão do CollectionsManager
    import core.collections_manager as cm_module
    original_path = cm_module.COLLECTIONS_FILE
    cm_module.COLLECTIONS_FILE = path
    
    yield path
    
    # Restaura caminho original
    cm_module.COLLECTIONS_FILE = original_path
    
    # Limpa arquivo temporário
    if os.path.exists(path):
        os.unlink(path)


class TestCollectionsCRUD:
    """Testes de CRUD de coleções."""
    
    def test_create_collection(self, temp_collections_file):
        """
        SMOKE TEST: Criar coleção deve persistir.
        """
        cm = CollectionsManager()
        
        result = cm.create_collection("My Collection")
        
        assert result is True
        assert "My Collection" in cm.collections
        assert cm.collections["My Collection"] == []
        
        # Recarregar e verificar persistência
        cm2 = CollectionsManager()
        assert "My Collection" in cm2.collections
    
    def test_create_duplicate_collection_fails(self, temp_collections_file):
        """
        EDGE CASE: Não pode criar coleção com nome duplicado.
        """
        cm = CollectionsManager()
        
        cm.create_collection("Duplicated")
        result = cm.create_collection("Duplicated")
        
        assert result is False
        assert cm.get_collection_size("Duplicated") == 0
    
    def test_rename_collection(self, temp_collections_file):
        """
        OPERAÇÃO: Renomear coleção deve manter projetos.
        """
        cm = CollectionsManager()
        
        cm.create_collection("Old Name")
        cm.add_project("Old Name", "/project1")
        cm.add_project("Old Name", "/project2")
        
        result = cm.rename_collection("Old Name", "New Name")
        
        assert result is True
        assert "Old Name" not in cm.collections
        assert "New Name" in cm.collections
        assert len(cm.collections["New Name"]) == 2
        assert "/project1" in cm.collections["New Name"]
    
    def test_delete_collection(self, temp_collections_file):
        """
        OPERAÇÃO: Deletar coleção deve persistir.
        """
        cm = CollectionsManager()
        
        cm.create_collection("To Delete")
        cm.add_project("To Delete", "/project1")
        
        result = cm.delete_collection("To Delete")
        
        assert result is True
        assert "To Delete" not in cm.collections
        
        # Verificar persistência
        cm2 = CollectionsManager()
        assert "To Delete" not in cm2.collections


class TestProjectManagement:
    """Testes de adição/remoção de projetos."""
    
    def test_add_project_to_collection(self, temp_collections_file):
        """
        SMOKE TEST: Adicionar projeto a coleção.
        """
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        
        result = cm.add_project("My Collection", "/path/to/project1")
        
        assert result is True
        assert "/path/to/project1" in cm.collections["My Collection"]
        assert cm.get_collection_size("My Collection") == 1
    
    def test_add_duplicate_project_fails(self, temp_collections_file):
        """
        EDGE CASE: Não pode adicionar mesmo projeto duas vezes.
        """
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        
        cm.add_project("My Collection", "/project1")
        result = cm.add_project("My Collection", "/project1")
        
        assert result is False
        assert cm.get_collection_size("My Collection") == 1
    
    def test_remove_project_from_collection(self, temp_collections_file):
        """
        OPERAÇÃO: Remover projeto de coleção.
        """
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        cm.add_project("My Collection", "/project1")
        cm.add_project("My Collection", "/project2")
        
        result = cm.remove_project("My Collection", "/project1")
        
        assert result is True
        assert "/project1" not in cm.collections["My Collection"]
        assert "/project2" in cm.collections["My Collection"]
        assert cm.get_collection_size("My Collection") == 1
    
    def test_get_project_collections(self, temp_collections_file):
        """
        QUERY: Listar coleções que contêm um projeto.
        """
        cm = CollectionsManager()
        cm.create_collection("Collection A")
        cm.create_collection("Collection B")
        cm.create_collection("Collection C")
        
        cm.add_project("Collection A", "/project1")
        cm.add_project("Collection B", "/project1")
        cm.add_project("Collection C", "/project2")
        
        collections = cm.get_project_collections("/project1")
        
        assert len(collections) == 2
        assert "Collection A" in collections
        assert "Collection B" in collections
        assert "Collection C" not in collections


class TestUtilities:
    """Testes de utilitários e limpeza."""
    
    def test_clean_orphan_projects(self, temp_collections_file):
        """
        UTILITÁRIO: Remover projetos deletados das coleções.
        """
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        cm.add_project("My Collection", "/project1")
        cm.add_project("My Collection", "/project2")
        cm.add_project("My Collection", "/project3")
        
        # Simular que apenas /project1 e /project3 ainda existem
        valid_paths = {"/project1", "/project3"}
        removed_count = cm.clean_orphan_projects(valid_paths)
        
        assert removed_count == 1  # /project2 foi removido
        assert "/project1" in cm.collections["My Collection"]
        assert "/project2" not in cm.collections["My Collection"]
        assert "/project3" in cm.collections["My Collection"]
        assert cm.get_collection_size("My Collection") == 2
    
    def test_get_stats(self, temp_collections_file):
        """
        UTILITÁRIO: Estatísticas do sistema de coleções.
        """
        cm = CollectionsManager()
        cm.create_collection("Collection A")
        cm.create_collection("Collection B")
        
        cm.add_project("Collection A", "/project1")
        cm.add_project("Collection A", "/project2")
        cm.add_project("Collection B", "/project1")  # projeto duplicado em outra coleção
        
        stats = cm.get_stats()
        
        assert stats["total_collections"] == 2
        assert stats["total_entries"] == 3  # 2 em A + 1 em B
        assert stats["unique_projects"] == 2  # /project1 e /project2 (únicos)


class TestEdgeCases:
    """Testes de casos extremos."""
    
    def test_add_to_nonexistent_collection_fails(self, temp_collections_file):
        """
        EDGE CASE: Adicionar a coleção inexistente deve falhar.
        """
        cm = CollectionsManager()
        
        result = cm.add_project("Nonexistent", "/project1")
        
        assert result is False
    
    def test_remove_from_nonexistent_collection_fails(self, temp_collections_file):
        """
        EDGE CASE: Remover de coleção inexistente deve falhar.
        """
        cm = CollectionsManager()
        
        result = cm.remove_project("Nonexistent", "/project1")
        
        assert result is False
    
    def test_get_collection_size_nonexistent(self, temp_collections_file):
        """
        EDGE CASE: Tamanho de coleção inexistente deve ser 0.
        """
        cm = CollectionsManager()
        
        size = cm.get_collection_size("Nonexistent")
        
        assert size == 0
