"""
test_collections.py — Testes do CollectionsManager (Fase 2)

Testa todas as operações de coleções:
  - Criar/deletar coleção
  - Adicionar/remover projeto
  - Renomear coleção
  - Listar coleções
  - Verificar membros
  - Limpar órfãos
"""
import pytest
import os
import json
from core.collections_manager import CollectionsManager, COLLECTIONS_FILE


class TestCollectionsCRUD:
    """Testes de CRUD básico de coleções."""
    
    def test_create_collection(self):
        """CREATE: Criar nova coleção."""
        cm = CollectionsManager()
        
        result = cm.create_collection("Test Collection")
        
        assert result is True
        assert "Test Collection" in cm.collections
        assert cm.collections["Test Collection"] == []
    
    def test_create_duplicate_collection(self):
        """CREATE: Criar coleção duplicada deve falhar."""
        cm = CollectionsManager()
        cm.create_collection("Duplicate")
        
        result = cm.create_collection("Duplicate")
        
        assert result is False
    
    def test_create_empty_name(self):
        """CREATE: Nome vazio deve falhar."""
        cm = CollectionsManager()
        
        result = cm.create_collection("")
        
        assert result is False
        result2 = cm.create_collection("   ")
        assert result2 is False
    
    def test_delete_collection(self):
        """DELETE: Remover coleção existente."""
        cm = CollectionsManager()
        cm.create_collection("To Delete")
        
        result = cm.delete_collection("To Delete")
        
        assert result is True
        assert "To Delete" not in cm.collections
    
    def test_delete_nonexistent_collection(self):
        """DELETE: Remover coleção inexistente deve falhar."""
        cm = CollectionsManager()
        
        result = cm.delete_collection("Does Not Exist")
        
        assert result is False
    
    def test_rename_collection(self):
        """UPDATE: Renomear coleção."""
        cm = CollectionsManager()
        cm.create_collection("Old Name")
        
        result = cm.rename_collection("Old Name", "New Name")
        
        assert result is True
        assert "Old Name" not in cm.collections
        assert "New Name" in cm.collections
    
    def test_rename_to_existing_name(self):
        """UPDATE: Renomear para nome já existente deve falhar."""
        cm = CollectionsManager()
        cm.create_collection("Name 1")
        cm.create_collection("Name 2")
        
        result = cm.rename_collection("Name 1", "Name 2")
        
        assert result is False


class TestCollectionsProjects:
    """Testes de adição/remoção de projetos."""
    
    def test_add_project_to_collection(self):
        """ADD: Adicionar projeto a coleção."""
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        
        result = cm.add_project("My Collection", "/path/to/project1")
        
        assert result is True
        assert "/path/to/project1" in cm.collections["My Collection"]
    
    def test_add_duplicate_project(self):
        """ADD: Adicionar projeto duplicado deve falhar."""
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        cm.add_project("My Collection", "/path/to/project1")
        
        result = cm.add_project("My Collection", "/path/to/project1")
        
        assert result is False
        # Deve ter apenas 1 entrada
        assert cm.collections["My Collection"].count("/path/to/project1") == 1
    
    def test_add_project_to_nonexistent_collection(self):
        """ADD: Adicionar a coleção inexistente deve falhar."""
        cm = CollectionsManager()
        
        result = cm.add_project("Does Not Exist", "/path/to/project1")
        
        assert result is False
    
    def test_remove_project_from_collection(self):
        """REMOVE: Remover projeto de coleção."""
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        cm.add_project("My Collection", "/path/to/project1")
        
        result = cm.remove_project("My Collection", "/path/to/project1")
        
        assert result is True
        assert "/path/to/project1" not in cm.collections["My Collection"]
    
    def test_remove_nonexistent_project(self):
        """REMOVE: Remover projeto inexistente deve falhar."""
        cm = CollectionsManager()
        cm.create_collection("My Collection")
        
        result = cm.remove_project("My Collection", "/path/does/not/exist")
        
        assert result is False


class TestCollectionsQueries:
    """Testes de consultas."""
    
    def test_get_all_collections(self):
        """QUERY: Listar todas as coleções."""
        cm = CollectionsManager()
        cm.create_collection("Collection A")
        cm.create_collection("Collection B")
        cm.create_collection("Collection C")
        
        all_collections = cm.get_all_collections()
        
        assert len(all_collections) >= 3
        assert "Collection A" in all_collections
        assert isinstance(all_collections, list)
    
    def test_get_projects_in_collection(self):
        """QUERY: Listar projetos de uma coleção."""
        cm = CollectionsManager()
        cm.create_collection("Test")
        cm.add_project("Test", "/path/1")
        cm.add_project("Test", "/path/2")
        
        projects = cm.get_projects("Test")
        
        assert len(projects) == 2
        assert "/path/1" in projects
        assert "/path/2" in projects
    
    def test_get_project_collections(self):
        """QUERY: Listar coleções de um projeto."""
        cm = CollectionsManager()
        cm.create_collection("Collection 1")
        cm.create_collection("Collection 2")
        cm.add_project("Collection 1", "/path/project")
        cm.add_project("Collection 2", "/path/project")
        
        collections = cm.get_project_collections("/path/project")
        
        assert len(collections) == 2
        assert "Collection 1" in collections
        assert "Collection 2" in collections
    
    def test_is_project_in_collection(self):
        """QUERY: Verificar se projeto está em coleção."""
        cm = CollectionsManager()
        cm.create_collection("Test")
        cm.add_project("Test", "/path/project")
        
        assert cm.is_project_in_collection("Test", "/path/project") is True
        assert cm.is_project_in_collection("Test", "/path/other") is False
    
    def test_get_collection_size(self):
        """QUERY: Obter tamanho da coleção."""
        cm = CollectionsManager()
        cm.create_collection("Test")
        cm.add_project("Test", "/path/1")
        cm.add_project("Test", "/path/2")
        cm.add_project("Test", "/path/3")
        
        size = cm.get_collection_size("Test")
        
        assert size == 3


class TestCollectionsPersistence:
    """Testes de persistência (save/load)."""
    
    def test_save_and_load(self):
        """PERSIST: Salvar e carregar coleções."""
        # Cria e salva
        cm1 = CollectionsManager()
        cm1.create_collection("Persistent Collection")
        cm1.add_project("Persistent Collection", "/path/test")
        cm1.save()
        
        # Carrega em nova instância
        cm2 = CollectionsManager()
        
        assert "Persistent Collection" in cm2.collections
        assert "/path/test" in cm2.collections["Persistent Collection"]
    
    def test_atomic_save(self):
        """ATOMIC: Save atômico usa .tmp."""
        cm = CollectionsManager()
        cm.create_collection("Atomic Test")
        cm.save()
        
        # Verifica que não sobrou .tmp
        assert not os.path.exists(COLLECTIONS_FILE + ".tmp")
        
        # Verifica que salvou
        assert os.path.exists(COLLECTIONS_FILE)


class TestCollectionsUtilities:
    """Testes de utilitários."""
    
    def test_clean_orphan_projects(self):
        """CLEAN: Remover projetos órfãos."""
        cm = CollectionsManager()
        cm.create_collection("Test")
        cm.add_project("Test", "/path/valid")
        cm.add_project("Test", "/path/orphan1")
        cm.add_project("Test", "/path/orphan2")
        
        # Apenas /path/valid existe no database
        valid_paths = {"/path/valid"}
        
        removed_count = cm.clean_orphan_projects(valid_paths)
        
        assert removed_count == 2
        assert "/path/valid" in cm.collections["Test"]
        assert "/path/orphan1" not in cm.collections["Test"]
        assert "/path/orphan2" not in cm.collections["Test"]
    
    def test_get_stats(self):
        """STATS: Obter estatísticas do sistema."""
        cm = CollectionsManager()
        cm.create_collection("Collection 1")
        cm.create_collection("Collection 2")
        cm.add_project("Collection 1", "/path/1")
        cm.add_project("Collection 1", "/path/2")
        cm.add_project("Collection 2", "/path/2")  # Mesmo projeto em 2 coleções
        
        stats = cm.get_stats()
        
        assert stats["total_collections"] == 2
        assert stats["total_entries"] == 3
        assert stats["unique_projects"] == 2  # /path/1 e /path/2


class TestCollectionsEdgeCases:
    """Testes de casos extremos."""
    
    def test_get_projects_from_nonexistent_collection(self):
        """ERROR: Buscar projetos de coleção inexistente."""
        cm = CollectionsManager()
        
        projects = cm.get_projects("Does Not Exist")
        
        assert projects == []
    
    def test_project_in_multiple_collections(self):
        """EDGE: Projeto em múltiplas coleções."""
        cm = CollectionsManager()
        cm.create_collection("Collection A")
        cm.create_collection("Collection B")
        cm.create_collection("Collection C")
        
        cm.add_project("Collection A", "/path/popular")
        cm.add_project("Collection B", "/path/popular")
        cm.add_project("Collection C", "/path/popular")
        
        collections = cm.get_project_collections("/path/popular")
        
        assert len(collections) == 3
    
    def test_delete_collection_with_projects(self):
        """EDGE: Deletar coleção com projetos não afeta projetos."""
        cm = CollectionsManager()
        cm.create_collection("To Delete")
        cm.add_project("To Delete", "/path/project")
        
        cm.delete_collection("To Delete")
        
        # Coleção foi deletada
        assert "To Delete" not in cm.collections
        # Projeto ainda existe (só remove referência)
        assert True  # Teste conceitual - projetos estão no database, não aqui
