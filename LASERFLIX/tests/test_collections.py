"""
test_collections.py — Testes do CollectionsManager (Fase 2)

Testa todas as operações de coleções:
  - Criar/deletar coleção
  - Adicionar/remover projeto
  - Renomear coleção
  - Listar coleções
  - Verificar membros
  - Limpar órfãos

NOTA: Usa patch para isolar testes do arquivo real collections.json.
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from core.collections_manager import CollectionsManager


def make_fresh_cm():
    """
    Cria CollectionsManager limpo (sem ler nem salvar arquivo real).
    Usa patch em load() e save() para isolar testes.
    """
    with patch.object(CollectionsManager, 'load', return_value=None), \
         patch.object(CollectionsManager, 'save', return_value=None):
        cm = CollectionsManager()
        cm.collections = {}  # Estado limpo
    return cm


class TestCollectionsCRUD:
    """Testes de CRUD básico de coleções."""
    
    def test_create_collection(self):
        """CREATE: Criar nova coleção."""
        cm = make_fresh_cm()
        
        with patch.object(cm, 'save'):
            result = cm.create_collection("Test Collection")
        
        assert result is True
        assert "Test Collection" in cm.collections
        assert cm.collections["Test Collection"] == []
    
    def test_create_duplicate_collection(self):
        """CREATE: Criar coleção duplicada deve falhar."""
        cm = make_fresh_cm()
        cm.collections["Duplicate"] = []
        
        with patch.object(cm, 'save'):
            result = cm.create_collection("Duplicate")
        
        assert result is False
    
    def test_create_empty_name(self):
        """CREATE: Nome vazio deve falhar."""
        cm = make_fresh_cm()
        
        with patch.object(cm, 'save'):
            result = cm.create_collection("")
            result2 = cm.create_collection("   ")
        
        assert result is False
        assert result2 is False
    
    def test_delete_collection(self):
        """DELETE: Remover coleção existente."""
        cm = make_fresh_cm()
        cm.collections["To Delete"] = []
        
        with patch.object(cm, 'save'):
            result = cm.delete_collection("To Delete")
        
        assert result is True
        assert "To Delete" not in cm.collections
    
    def test_delete_nonexistent_collection(self):
        """DELETE: Remover coleção inexistente deve falhar."""
        cm = make_fresh_cm()
        
        with patch.object(cm, 'save'):
            result = cm.delete_collection("Does Not Exist")
        
        assert result is False
    
    def test_rename_collection(self):
        """UPDATE: Renomear coleção."""
        cm = make_fresh_cm()
        cm.collections["Old Name"] = ["/path/1"]
        
        with patch.object(cm, 'save'):
            result = cm.rename_collection("Old Name", "New Name")
        
        assert result is True
        assert "Old Name" not in cm.collections
        assert "New Name" in cm.collections
        assert "/path/1" in cm.collections["New Name"]  # Projetos preservados
    
    def test_rename_to_existing_name(self):
        """UPDATE: Renomear para nome já existente deve falhar."""
        cm = make_fresh_cm()
        cm.collections["Name 1"] = []
        cm.collections["Name 2"] = []
        
        with patch.object(cm, 'save'):
            result = cm.rename_collection("Name 1", "Name 2")
        
        assert result is False


class TestCollectionsProjects:
    """Testes de adição/remoção de projetos."""
    
    def test_add_project_to_collection(self):
        """ADD: Adicionar projeto a coleção."""
        cm = make_fresh_cm()
        cm.collections["My Collection"] = []
        
        with patch.object(cm, 'save'):
            result = cm.add_project("My Collection", "/path/to/project1")
        
        assert result is True
        assert "/path/to/project1" in cm.collections["My Collection"]
    
    def test_add_duplicate_project(self):
        """ADD: Adicionar projeto duplicado deve falhar."""
        cm = make_fresh_cm()
        cm.collections["My Collection"] = ["/path/to/project1"]
        
        with patch.object(cm, 'save'):
            result = cm.add_project("My Collection", "/path/to/project1")
        
        assert result is False
        assert cm.collections["My Collection"].count("/path/to/project1") == 1
    
    def test_add_project_to_nonexistent_collection(self):
        """ADD: Adicionar a coleção inexistente deve falhar."""
        cm = make_fresh_cm()
        
        with patch.object(cm, 'save'):
            result = cm.add_project("Does Not Exist", "/path/to/project1")
        
        assert result is False
    
    def test_remove_project_from_collection(self):
        """REMOVE: Remover projeto de coleção."""
        cm = make_fresh_cm()
        cm.collections["My Collection"] = ["/path/to/project1"]
        
        with patch.object(cm, 'save'):
            result = cm.remove_project("My Collection", "/path/to/project1")
        
        assert result is True
        assert "/path/to/project1" not in cm.collections["My Collection"]
    
    def test_remove_nonexistent_project(self):
        """REMOVE: Remover projeto inexistente deve falhar."""
        cm = make_fresh_cm()
        cm.collections["My Collection"] = []
        
        with patch.object(cm, 'save'):
            result = cm.remove_project("My Collection", "/path/does/not/exist")
        
        assert result is False


class TestCollectionsQueries:
    """Testes de consultas."""
    
    def test_get_all_collections(self):
        """QUERY: Listar todas as coleções (ordenadas)."""
        cm = make_fresh_cm()
        cm.collections = {
            "Collection C": [],
            "Collection A": [],
            "Collection B": [],
        }
        
        all_collections = cm.get_all_collections()
        
        assert all_collections == ["Collection A", "Collection B", "Collection C"]
    
    def test_get_projects_in_collection(self):
        """QUERY: Listar projetos de uma coleção."""
        cm = make_fresh_cm()
        cm.collections["Test"] = ["/path/1", "/path/2"]
        
        projects = cm.get_projects("Test")
        
        assert len(projects) == 2
        assert "/path/1" in projects
        assert "/path/2" in projects
    
    def test_get_project_collections(self):
        """QUERY: Listar coleções que contêm um projeto."""
        cm = make_fresh_cm()
        cm.collections = {
            "Collection 1": ["/path/project"],
            "Collection 2": ["/path/project"],
            "Collection 3": ["/path/other"],
        }
        
        collections = cm.get_project_collections("/path/project")
        
        assert len(collections) == 2
        assert "Collection 1" in collections
        assert "Collection 2" in collections
        assert "Collection 3" not in collections
    
    def test_is_project_in_collection(self):
        """QUERY: Verificar se projeto está em coleção."""
        cm = make_fresh_cm()
        cm.collections["Test"] = ["/path/project"]
        
        assert cm.is_project_in_collection("Test", "/path/project") is True
        assert cm.is_project_in_collection("Test", "/path/other") is False
    
    def test_get_collection_size(self):
        """QUERY: Obter tamanho exato da coleção."""
        cm = make_fresh_cm()
        cm.collections["Test"] = ["/path/1", "/path/2", "/path/3"]
        
        size = cm.get_collection_size("Test")
        
        assert size == 3


class TestCollectionsPersistence:
    """Testes de persistência (save/load)."""
    
    def test_save_and_load(self):
        """PERSIST: Salvar e recarregar coleções."""
        cm = make_fresh_cm()
        cm.collections["Persist Test"] = ["/path/test"]
        
        # Salva real (não mockado)
        cm.save()
        
        # Carrega em nova instância (load real)
        cm2 = CollectionsManager()
        
        assert "Persist Test" in cm2.collections
        assert "/path/test" in cm2.collections["Persist Test"]
    
    def test_atomic_save_no_tmp_leftover(self):
        """ATOMIC: Save atômico não deixa .tmp para trás."""
        from core.collections_manager import COLLECTIONS_FILE
        
        cm = make_fresh_cm()
        cm.save()
        
        assert not os.path.exists(COLLECTIONS_FILE + ".tmp")


class TestCollectionsUtilities:
    """Testes de utilitários."""
    
    def test_clean_orphan_projects(self):
        """CLEAN: Remover exatamente os projetos órfãos."""
        cm = make_fresh_cm()
        cm.collections["Test"] = ["/path/valid", "/path/orphan1", "/path/orphan2"]
        
        with patch.object(cm, 'save'):
            removed_count = cm.clean_orphan_projects({"/path/valid"})
        
        assert removed_count == 2
        assert "/path/valid" in cm.collections["Test"]
        assert "/path/orphan1" not in cm.collections["Test"]
        assert "/path/orphan2" not in cm.collections["Test"]
    
    def test_get_stats(self):
        """STATS: Estatísticas corretas de coleções isoladas."""
        cm = make_fresh_cm()
        cm.collections = {
            "Collection 1": ["/path/1", "/path/2"],
            "Collection 2": ["/path/2"],  # /path/2 em 2 coleções
        }
        
        stats = cm.get_stats()
        
        assert stats["total_collections"] == 2
        assert stats["total_entries"] == 3
        assert stats["unique_projects"] == 2  # /path/1 e /path/2


class TestCollectionsEdgeCases:
    """Testes de casos extremos."""
    
    def test_get_projects_from_nonexistent_collection(self):
        """ERROR: Buscar projetos de coleção inexistente retorna lista vazia."""
        cm = make_fresh_cm()
        
        projects = cm.get_projects("Does Not Exist")
        
        assert projects == []
    
    def test_project_in_multiple_collections(self):
        """EDGE: Projeto pode estar em múltiplas coleções."""
        cm = make_fresh_cm()
        cm.collections = {
            "Collection A": ["/path/popular"],
            "Collection B": ["/path/popular"],
            "Collection C": ["/path/popular"],
        }
        
        collections = cm.get_project_collections("/path/popular")
        
        assert len(collections) == 3
    
    def test_delete_collection_with_projects(self):
        """EDGE: Deletar coleção com projetos remove apenas a coleção."""
        cm = make_fresh_cm()
        cm.collections["To Delete"] = ["/path/project"]
        
        with patch.object(cm, 'save'):
            result = cm.delete_collection("To Delete")
        
        assert result is True
        assert "To Delete" not in cm.collections
        # Projeto não é afetado (está no database, não aqui)
