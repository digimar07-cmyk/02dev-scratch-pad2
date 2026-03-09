"""
test_database.py — Testes do DatabaseManager (Fase 2)

Testa todas as operações do banco de dados:
  - Criar/carregar database
  - Adicionar/atualizar projetos (via self.database)
  - Salvar/carregar JSON
  - Backups automáticos
"""
import pytest
import os
import json
from core.database import DatabaseManager


class TestDatabaseBasics:
    """Testes básicos de criação e carregamento."""
    
    def test_create_empty_database(self, temp_db_file):
        """SMOKE: Criar DatabaseManager com arquivo vazio."""
        db = DatabaseManager(db_file=temp_db_file)
        
        assert db is not None
        assert isinstance(db.database, dict)
        assert len(db.database) == 0
    
    def test_load_existing_database(self, temp_db_file, sample_database):
        """LOAD: Carregar database existente."""
        # Salva dados de exemplo
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        # Carrega
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        assert len(db.database) == 3
        assert "/path/to/project1" in db.database
        assert db.database["/path/to/project1"]["name"] == "Christmas Tree"


class TestDatabaseManipulation:
    """Testes de manipulação direta do dicionário."""
    
    def test_add_project_manually(self, temp_db_file):
        """MANUAL: Adicionar projeto via self.database."""
        db = DatabaseManager(db_file=temp_db_file)
        
        project_path = "/path/to/new_project"
        project_data = {
            "name": "New Project",
            "origin": "Etsy",
            "favorite": False,
            "categories": ["Test"],
            "tags": ["new"],
        }
        
        # Adiciona diretamente ao dict
        db.database[project_path] = project_data
        
        assert project_path in db.database
        assert db.database[project_path]["name"] == "New Project"
    
    def test_update_project_manually(self, temp_db_file, sample_database):
        """UPDATE: Atualizar projeto via self.database."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        # Atualiza
        db.database["/path/to/project1"]["favorite"] = True
        
        # Verifica
        assert db.database["/path/to/project1"]["favorite"] is True
    
    def test_delete_project_manually(self, temp_db_file, sample_database):
        """DELETE: Remover projeto via del."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        # Deleta
        del db.database["/path/to/project1"]
        
        # Verifica
        assert "/path/to/project1" not in db.database
        assert len(db.database) == 2


class TestDatabaseQueries:
    """Testes de consultas usando operações de dicionário."""
    
    def test_get_all_projects(self, temp_db_file, sample_database):
        """QUERY: Listar todos os projetos (items())."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        all_projects = list(db.database.items())
        
        assert len(all_projects) == 3
        assert isinstance(all_projects, list)
    
    def test_filter_favorites(self, temp_db_file, sample_database):
        """FILTER: Filtrar favoritos usando list comprehension."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        favorites = [(p, d) for p, d in db.database.items() if d.get("favorite")]
        
        assert len(favorites) == 1
        assert favorites[0][1]["name"] == "Wooden Box"
    
    def test_search_by_name(self, temp_db_file, sample_database):
        """SEARCH: Buscar por nome usando filter."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        query = "box"
        results = [
            (p, d) for p, d in db.database.items()
            if query.lower() in d.get("name", "").lower()
        ]
        
        assert len(results) >= 1
        assert any("Box" in d["name"] for _, d in results)


class TestDatabasePersistence:
    """Testes de persistência (salvar/carregar JSON)."""
    
    def test_save_database(self, temp_db_file):
        """PERSIST: Salvar database em JSON."""
        db = DatabaseManager(db_file=temp_db_file)
        
        # Adiciona projeto
        db.database["/path/test"] = {"name": "Test"}
        
        # Salva
        db.save_database()
        
        # Verifica que arquivo foi criado
        assert os.path.exists(temp_db_file)
        
        # Carrega novamente e verifica
        db2 = DatabaseManager(db_file=temp_db_file)
        db2.load_database()
        assert "/path/test" in db2.database
    
    def test_atomic_save(self, temp_db_file):
        """ATOMIC: Save atômico cria .tmp antes de replace."""
        db = DatabaseManager(db_file=temp_db_file)
        db.database["/path/atomic"] = {"name": "Atomic Test"}
        
        # Salva (internamente usa _save_json_atomic)
        db.save_database()
        
        # Verifica que não sobrou arquivo .tmp
        assert not os.path.exists(temp_db_file + ".tmp")
        
        # Verifica que salvou corretamente
        with open(temp_db_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "/path/atomic" in data
    
    def test_backup_created(self, temp_db_file):
        """BACKUP: Salvar cria arquivo .bak."""
        db = DatabaseManager(db_file=temp_db_file)
        db.database["/path/1"] = {"name": "First"}
        db.save_database()
        
        # Modifica e salva novamente (deve criar .bak)
        db.database["/path/2"] = {"name": "Second"}
        db.save_database()
        
        # Verifica que .bak existe
        backup_file = temp_db_file + ".bak"
        assert os.path.exists(backup_file)


class TestDatabaseMigration:
    """Testes de migração de schema (category → categories)."""
    
    def test_migrate_old_schema(self, temp_db_file):
        """MIGRATION: Converter 'category' (string) → 'categories' (list)."""
        # Cria database no formato antigo
        old_data = {
            "/path/old": {
                "name": "Old Project",
                "category": "Natal",  # ← Formato antigo (string)
            }
        }
        
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(old_data, f)
        
        # Carrega (deve migrar automaticamente)
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        # Verifica que migrou
        project = db.database["/path/old"]
        assert "categories" in project
        assert isinstance(project["categories"], list)
        assert "Natal" in project["categories"]
        assert "category" not in project  # Campo antigo removido


class TestDatabaseConfig:
    """Testes de configuração (pastas e modelos)."""
    
    def test_load_empty_config(self, temp_db_file):
        """CONFIG: Carregar config vazio (arquivo não existe)."""
        # Config file que não existe
        config_file = temp_db_file + ".config.json"
        
        db = DatabaseManager(db_file=temp_db_file, config_file=config_file)
        db.load_config()
        
        # Deve iniciar com padrão vazio
        assert "folders" in db.config
        assert isinstance(db.config["folders"], list)
    
    def test_save_config(self, temp_db_file):
        """CONFIG: Salvar configuração."""
        config_file = temp_db_file + ".config.json"
        
        db = DatabaseManager(db_file=temp_db_file, config_file=config_file)
        db.config["folders"] = ["/path/folder1", "/path/folder2"]
        
        db.save_config()
        
        # Verifica que salvou
        assert os.path.exists(config_file)
        
        # Carrega novamente
        db2 = DatabaseManager(db_file=temp_db_file, config_file=config_file)
        db2.load_config()
        assert len(db2.config["folders"]) == 2


class TestDatabaseEdgeCases:
    """Testes de casos extremos e erros."""
    
    def test_get_nonexistent_project(self, temp_db_file, sample_database):
        """ERROR: Buscar projeto que não existe."""
        with open(temp_db_file, 'w', encoding='utf-8') as f:
            json.dump(sample_database, f)
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()
        
        project = db.database.get("/path/does/not/exist")
        assert project is None
    
    def test_corrupted_json(self, temp_db_file):
        """ERROR: Carregar JSON corrompido."""
        # Escreve JSON inválido
        with open(temp_db_file, 'w') as f:
            f.write("{invalid json")
        
        db = DatabaseManager(db_file=temp_db_file)
        db.load_database()  # Não deve crashar
        
        # Deve iniciar vazio após erro
        assert len(db.database) == 0
