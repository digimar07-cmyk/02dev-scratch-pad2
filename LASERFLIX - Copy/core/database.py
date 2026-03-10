"""
Gerenciamento de banco de dados JSON
"""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from typing import Any, Iterator
from config.settings import DB_FILE, CONFIG_FILE, BACKUP_FOLDER, MAX_AUTO_BACKUPS
from utils.logging_setup import LOGGER


class DatabaseManager:
    """
    Gerencia persistência de dados em JSON com backups automáticos.

    API pública (VOLKOV-01):
      get_project(path)         → dict | None
      set_project(path, data)   → None
      remove_project(path)      → bool
      has_project(path)         → bool
      all_paths()               → list[str]
      all_projects()            → dict (cópia)
      project_count()           → int
      iter_projects()           → Iterator[(str, dict)]
    """

    def __init__(self, db_file: str | None = None, config_file: str | None = None) -> None:
        """
        Args:
            db_file: Caminho customizado para database.json (usado em testes)
            config_file: Caminho customizado para config.json (usado em testes)
        """
        self.database: dict[str, dict[str, Any]] = {}
        self.config: dict[str, Any] = {"folders": [], "models": {}}
        self.logger = LOGGER

        self.db_file: str = db_file or DB_FILE
        self.config_file: str = config_file or CONFIG_FILE

        os.makedirs(BACKUP_FOLDER, exist_ok=True)

    # ── API Pública (VOLKOV-01) ───────────────────────────────────────────────

    def get_project(self, path: str) -> dict[str, Any] | None:
        """Retorna dados de um projeto pelo caminho. None se não encontrado."""
        return self.database.get(path)

    def set_project(self, path: str, data: dict[str, Any]) -> None:
        """Insere ou atualiza um projeto."""
        self.database[path] = data

    def remove_project(self, path: str) -> bool:
        """Remove um projeto. Retorna True se removido, False se não existia."""
        if path not in self.database:
            return False
        del self.database[path]
        return True

    def has_project(self, path: str) -> bool:
        """Verifica se um caminho existe no banco."""
        return path in self.database

    def all_paths(self) -> list[str]:
        """Retorna lista de todos os caminhos registrados."""
        return list(self.database.keys())

    def all_projects(self) -> dict[str, dict[str, Any]]:
        """Retorna cópia do dicionário completo. Nunca a referência interna."""
        return dict(self.database)

    def project_count(self) -> int:
        """Retorna total de projetos."""
        return len(self.database)

    def iter_projects(self) -> Iterator[tuple[str, dict[str, Any]]]:
        """Itera sobre (path, data) de todos os projetos."""
        return iter(self.database.items())

    # ── Persistência ─────────────────────────────────────────────────────────

    def load_config(self) -> None:
        """
        Carrega configurações de pastas e modelos.
        Cria arquivo padrão se não existir.
        """
        if not os.path.exists(self.config_file):
            self.logger.info("⚠️ Config não encontrado, usando padrão vazio")
            return

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            self.logger.info("✅ Config carregado: %d pastas", len(self.config.get("folders", [])))

        except json.JSONDecodeError as e:
            self.logger.error(
                "Arquivo config corrompido (JSON inválido): %s. Usando backup se disponível.",
                e, exc_info=True
            )
            self._try_restore_from_backup(self.config_file)

        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(
                "Erro de acesso ao config: %s. Usando padrão vazio.",
                e, exc_info=True
            )

        except UnicodeDecodeError as e:
            self.logger.error(
                "Erro de encoding no config: %s. Tentando com latin-1.",
                e, exc_info=True
            )
            try:
                with open(self.config_file, "r", encoding="latin-1") as f:
                    self.config = json.load(f)
                self.logger.info("✅ Config carregado com encoding alternativo")
            except Exception as fallback_err:
                self.logger.error("Falha no fallback de encoding: %s", fallback_err)

    def save_config(self) -> None:
        """Salva configurações de forma atômica."""
        self._save_json_atomic(self.config_file, self.config, make_backup=True)

    def load_database(self) -> None:
        """
        Carrega banco de dados. Migra campo 'category' → 'categories' se necessário.
        """
        if not os.path.exists(self.db_file):
            self.logger.info("⚠️ Database não encontrado, iniciando vazio")
            return

        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                self.database = json.load(f)

            for path, data in self.database.items():
                if "category" in data and "categories" not in data:
                    old_cat = data.get("category", "")
                    data["categories"] = [old_cat] if (old_cat and old_cat != "Sem Categoria") else []
                    del data["category"]

            self.logger.info("✅ Database carregado: %d projetos", len(self.database))

        except json.JSONDecodeError as e:
            self.logger.error(
                "Database corrompido (JSON inválido): %s. Tentando restaurar backup.",
                e, exc_info=True
            )
            self._try_restore_from_backup(self.db_file)

        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(
                "Erro de acesso ao database: %s. Iniciando vazio.",
                e, exc_info=True
            )

        except UnicodeDecodeError as e:
            self.logger.error(
                "Erro de encoding no database: %s. Tentando encoding alternativo.",
                e, exc_info=True
            )
            try:
                with open(self.db_file, "r", encoding="latin-1") as f:
                    self.database = json.load(f)
                self.logger.info("✅ Database carregado com encoding alternativo")
            except Exception as fallback_err:
                self.logger.error("Falha no fallback de encoding: %s", fallback_err)

    def save_database(self) -> None:
        """Salva banco de dados de forma atômica."""
        self._save_json_atomic(self.db_file, self.database, make_backup=True)

    # ── Backup ────────────────────────────────────────────────────────────────

    def auto_backup(self) -> None:
        """Cria backup automático com timestamp. Limita a MAX_AUTO_BACKUPS arquivos."""
        if not os.path.exists(self.db_file):
            self.logger.debug("Database não existe, pulando auto-backup")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_FOLDER, f"auto_backup_{timestamp}.json")
            shutil.copy2(self.db_file, backup_file)

            try:
                backups = sorted([
                    f for f in os.listdir(BACKUP_FOLDER)
                    if f.startswith("auto_backup_")
                ])
                if len(backups) > MAX_AUTO_BACKUPS:
                    for old_backup in backups[:-MAX_AUTO_BACKUPS]:
                        os.remove(os.path.join(BACKUP_FOLDER, old_backup))
            except OSError as cleanup_err:
                self.logger.warning("Falha ao limpar backups antigos: %s", cleanup_err)

            self.logger.info("💾 Auto-backup criado: %s", backup_file)

        except (OSError, PermissionError) as e:
            self.logger.error("Falha no auto-backup: %s", e, exc_info=True)

    def manual_backup(self) -> str | None:
        """Cria backup manual com confirmação. Retorna caminho do backup ou None."""
        if not os.path.exists(self.db_file):
            self.logger.warning("Database não existe, nada para fazer backup")
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_FOLDER, f"manual_backup_{timestamp}.json")
            shutil.copy2(self.db_file, backup_file)
            self.logger.info("💾 Backup manual: %s", backup_file)
            return backup_file

        except (OSError, PermissionError) as e:
            self.logger.error("Erro em manual_backup: %s", e, exc_info=True)
            return None

    # ── Internos ──────────────────────────────────────────────────────────────

    def _save_json_atomic(self, filepath: str, data: Any, make_backup: bool = True) -> None:
        """Salva JSON com estratégia atômica (write + rename)."""
        tmp_file = filepath + ".tmp"

        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            if make_backup and os.path.exists(filepath):
                try:
                    shutil.copy2(filepath, filepath + ".bak")
                except (PermissionError, OSError) as bak_err:
                    self.logger.warning(
                        "Não foi possível criar .bak de %s: %s", filepath, bak_err
                    )

            os.replace(tmp_file, filepath)

        except (IOError, OSError, PermissionError) as e:
            self.logger.error(
                "Falha ao salvar JSON atômico em %s: %s", filepath, e, exc_info=True
            )
            try:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
            except OSError:
                pass
            raise

        except TypeError as e:
            self.logger.error(
                "Dados não serializáveis para JSON em %s: %s", filepath, e, exc_info=True
            )
            raise

    def _try_restore_from_backup(self, filepath: str) -> bool:
        """Tenta restaurar arquivo a partir do .bak mais recente."""
        backup_file = filepath + ".bak"

        if not os.path.exists(backup_file):
            self.logger.warning(
                "Arquivo .bak não encontrado para %s. Impossível restaurar.", filepath
            )
            return False

        try:
            shutil.copy2(backup_file, filepath)
            self.logger.info("✅ Arquivo restaurado de %s", backup_file)

            if filepath == self.db_file:
                self.load_database()
            elif filepath == self.config_file:
                self.load_config()

            return True

        except (OSError, PermissionError) as e:
            self.logger.error(
                "Falha ao restaurar backup de %s: %s", backup_file, e, exc_info=True
            )
            return False
