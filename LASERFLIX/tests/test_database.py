"""
test_database.py — Testes do DatabaseManager (Fase 2)

Testa todas as operações CRUD do banco de dados:
  - Criar/carregar database
  - Adicionar projeto
  - Atualizar projeto
  - Buscar projeto
  - Listar todos
  - Favoritar/desfavoritar
  - Deletar projeto
  - Salvar em JSON
"""
import pytest
import os
import json
from core.database import DatabaseManager


class TestDatabaseBasics:
    """Testes básicos de criação e carregamento."""
    
    def test_create_empty_database(self, temp_db_file):
        """SMOKE: Criar database vazio."""
        db = DatabaseManager(temp_db_file)
        
        assert db is not None
        assert len(db.data) == 0
    
    def test_load_existing_database(self, temp_db_file, sample_database):
        """LOAD: Carregar database existente."""
        # Salva dados de exemplo
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        # Carrega
        db = DatabaseManager(temp_db_file)
        
        assert len(db.data) == 3
        assert "/path/to/project1" in db.data


class TestDatabaseCRUD:
    """Testes de operações CRUD (Create, Read, Update, Delete)."""
    
    def test_add_project(self, temp_db_file):
        """CREATE: Adicionar novo projeto."""
        db = DatabaseManager(temp_db_file)
        
        project_path = "/path/to/new_project"
        project_data = {
            "name": "New Project",
            "origin": "Etsy",
            "favorite": False,
            "categories": ["Test"],
            "tags": ["new"],
        }
        
        db.add_project(project_path, project_data)
        
        assert project_path in db.data
        assert db.data[project_path]["name"] == "New Project"
    
    def test_get_project(self, temp_db_file, sample_database):
        """READ: Buscar projeto por path."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        project = db.get_project("/path/to/project1")
        
        assert project is not None
        assert project["name"] == "Christmas Tree"
    
    def test_update_project(self, temp_db_file, sample_database):
        """UPDATE: Atualizar dados de projeto existente."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        # Atualiza
        db.update_project("/path/to/project1", {"favorite": True})
        
        # Verifica
        project = db.get_project("/path/to/project1")
        assert project["favorite"] is True
    
    def test_delete_project(self, temp_db_file, sample_database):
        """DELETE: Remover projeto."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        # Deleta
        db.delete_project("/path/to/project1")
        
        # Verifica
        assert "/path/to/project1" not in db.data
        assert len(db.data) == 2


class TestDatabaseQueries:
    """Testes de consultas e filtros."""
    
    def test_get_all_projects(self, temp_db_file, sample_database):
        """QUERY: Listar todos os projetos."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        all_projects = db.get_all_projects()
        
        assert len(all_projects) == 3
        assert isinstance(all_projects, list)
    
    def test_get_favorites(self, temp_db_file, sample_database):
        """FILTER: Filtrar apenas favoritos."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        favorites = db.get_favorites()
        
        assert len(favorites) == 1
        assert favorites[0][1]["name"] == "Wooden Box"
    
    def test_search_by_name(self, temp_db_file, sample_database):
        """SEARCH: Buscar por nome."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        results = db.search("box")
        
        assert len(results) >= 1
        assert any("Box" in p[1]["name"] for p in results)


class TestDatabaseFlags:
    """Testes de flags (favorite, done, good, bad)."""
    
    def test_toggle_favorite(self, temp_db_file, sample_database):
        """FLAG: Toggle favorite."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        path = "/path/to/project1"
        
        # Inicialmente False
        assert db.data[path]["favorite"] is False
        
        # Toggle para True
        db.toggle_favorite(path)
        assert db.data[path]["favorite"] is True
        
        # Toggle de volta para False
        db.toggle_favorite(path)
        assert db.data[path]["favorite"] is False
    
    def test_mark_as_done(self, temp_db_file, sample_database):
        """FLAG: Marcar como feito."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(temp_db_file)
        
        path = "/path/to/project1"
        db.mark_as_done(path)
        
        assert db.data[path]["done"] is True


class TestDatabasePersistence:
    """Testes de persistência (salvar/carregar JSON)."""
    
    def test_save_to_json(self, temp_db_file):
        """PERSIST: Salvar alterações em JSON."""
        db = DatabaseManager(temp_db_file)
        
        # Adiciona projeto
        db.add_project("/path/test", {"name": "Test"})
        
        # Salva
        db.save()
        
        # Verifica que arquivo foi criado
        assert os.path.exists(temp_db_file)
        
        # Carrega novamente e verifica
        db2 = DatabaseManager(temp_db_file)
        assert "/path/test" in db2.data
    
    def test_auto_save_on_changes(self, temp_db_file):
        """PERSIST: Auto-save após mudanças."""
        db = DatabaseManager(temp_db_file)
        
        # Adiciona (deve auto-save se implementado)
        db.add_project("/path/auto", {"name": "Auto"})
        
        # Carrega em nova instância
        db2 = DatabaseManager(temp_db_file)
        
        # Se auto-save funciona, deve estar lá
        assert "/path/auto" in db2.data


class TestDatabaseEdgeCases:
    """Testes de casos extremos e erros."""
    
    def test_get_nonexistent_project(self, temp_db_file):
        """ERROR: Buscar projeto que não existe."""
        db = DatabaseManager(temp_db_file)
        
        project = db.get_project("/path/does/not/exist")
        
        assert project is None
    
    def test_delete_nonexistent_project(self, temp_db_file):
        """ERROR: Deletar projeto que não existe (não deve crashar)."""
        db = DatabaseManager(temp_db_file)
        
        # Não deve lançar exceção
        db.delete_project("/path/does/not/exist")
        
        assert True  # Se chegou aqui, não crashou
    
    def test_update_nonexistent_project(self, temp_db_file):
        """ERROR: Atualizar projeto que não existe."""
        db = DatabaseManager(temp_db_file)
        
        # Não deve crashar
        db.update_project("/path/does/not/exist", {"name": "New"})
        
        assert True
