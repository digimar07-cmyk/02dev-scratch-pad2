"""
core/collections_manager.py — Gerenciador de Coleções/Playlists.

Sistema para agrupar projetos em coleções temáticas.
Projetos podem estar em múltiplas coleções simultaneamente.

Arquitetura Kent Beck:
- Métodos atômicos (uma responsabilidade por método)
- Sem dependência de UI (100% testável)
- API clara e previsível
- file_path injetável no __init__ (testabilidade, DIP)
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Set
from config.settings import DB_FILE
from utils.logging_setup import LOGGER


COLLECTIONS_FILE = os.path.join(os.path.dirname(DB_FILE), "collections.json")


class CollectionsManager:
    """
    Gerencia coleções de projetos.

    Estrutura de dados:
    {
        "collection_name": ["path/to/project1", "path/to/project2", ...],
        ...
    }

    Coleções são armazenadas separadamente do database principal
    para evitar poluição do schema de projetos.

    Args:
        file_path: Caminho customizado para collections.json.
                   Se None, usa COLLECTIONS_FILE (default de produção).
                   Injetar em testes garante isolamento e sem side-effects.
    """

    def __init__(self, file_path: str | None = None) -> None:
        self.file_path: str = file_path or COLLECTIONS_FILE
        self.collections: Dict[str, List[str]] = {}
        self.logger = LOGGER
        self.load()

    def load(self) -> None:
        """
        Carrega coleções do disco.
        Cria arquivo vazio se não existir.
        """
        if not os.path.exists(self.file_path):
            self.logger.info("ℹ️ Collections file não existe, criando vazio")
            self.save()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.collections = json.load(f)
            self.logger.info(
                "✅ Collections carregado: %d coleções",
                len(self.collections)
            )

        except json.JSONDecodeError as e:
            self.logger.error(
                "⚠️ Collections corrompido: %s. Iniciando vazio.",
                e, exc_info=True
            )
            self.collections = {}

        except Exception as e:
            self.logger.error(
                "⚠️ Erro ao carregar collections: %s",
                e, exc_info=True
            )
            self.collections = {}

    def save(self) -> None:
        """
        Salva coleções no disco de forma atômica.
        """
        tmp_file = self.file_path + ".tmp"

        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(self.collections, f, indent=2, ensure_ascii=False)

            os.replace(tmp_file, self.file_path)
            self.logger.debug("💾 Collections salvo: %d coleções", len(self.collections))

        except Exception as e:
            self.logger.error(
                "⚠️ Erro ao salvar collections: %s",
                e, exc_info=True
            )
            if os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except OSError:
                    pass

    # === CRUD de Coleções ===

    def add_collection(self, name: str) -> bool:
        """Alias para create_collection() (compatibilidade com UI)."""
        return self.create_collection(name)

    def create_collection(self, name: str) -> bool:
        """
        Cria nova coleção vazia.

        Returns:
            True se criada com sucesso, False se já existe
        """
        name = name.strip()

        if not name:
            self.logger.warning("⚠️ Nome de coleção vazio")
            return False

        if name in self.collections:
            self.logger.warning("⚠️ Coleção '%s' já existe", name)
            return False

        self.collections[name] = []
        self.save()
        self.logger.info("✨ Coleção criada: %s", name)
        return True

    def rename_collection(self, old_name: str, new_name: str) -> bool:
        """
        Renomeia coleção existente.

        Returns:
            True se renomeada com sucesso
        """
        new_name = new_name.strip()

        if not new_name:
            self.logger.warning("⚠️ Novo nome vazio")
            return False

        if old_name not in self.collections:
            self.logger.warning("⚠️ Coleção '%s' não existe", old_name)
            return False

        if new_name in self.collections and new_name != old_name:
            self.logger.warning("⚠️ Nome '%s' já em uso", new_name)
            return False

        self.collections[new_name] = self.collections.pop(old_name)
        self.save()
        self.logger.info("✏️ Coleção renomeada: %s → %s", old_name, new_name)
        return True

    def delete_collection(self, name: str) -> bool:
        """
        Remove coleção (não apaga projetos, apenas a coleção).

        Returns:
            True se removida com sucesso
        """
        if name not in self.collections:
            self.logger.warning("⚠️ Coleção '%s' não existe", name)
            return False

        del self.collections[name]
        self.save()
        self.logger.info("🗑️ Coleção removida: %s", name)
        return True

    def get_all_collections(self) -> List[str]:
        """Retorna lista de nomes de coleções (ordenada)."""
        return sorted(self.collections.keys())

    def get_collection_size(self, name: str) -> int:
        """Retorna quantidade de projetos na coleção."""
        return len(self.collections.get(name, []))

    # === Gestão de Projetos ===

    def add_project(self, collection_name: str, project_path: str) -> bool:
        """
        Adiciona projeto a uma coleção.

        Returns:
            True se adicionado com sucesso
        """
        if collection_name not in self.collections:
            self.logger.warning("⚠️ Coleção '%s' não existe", collection_name)
            return False

        if project_path in self.collections[collection_name]:
            self.logger.debug("ℹ️ Projeto já está na coleção '%s'", collection_name)
            return False

        self.collections[collection_name].append(project_path)
        self.save()
        self.logger.info(
            "➕ Projeto adicionado a '%s': %s",
            collection_name, os.path.basename(project_path)
        )
        return True

    def remove_project(self, collection_name: str, project_path: str) -> bool:
        """
        Remove projeto de uma coleção.

        Returns:
            True se removido com sucesso
        """
        if collection_name not in self.collections:
            self.logger.warning("⚠️ Coleção '%s' não existe", collection_name)
            return False

        if project_path not in self.collections[collection_name]:
            self.logger.debug("ℹ️ Projeto não está na coleção '%s'", collection_name)
            return False

        self.collections[collection_name].remove(project_path)
        self.save()
        self.logger.info(
            "➖ Projeto removido de '%s': %s",
            collection_name, os.path.basename(project_path)
        )
        return True

    def get_projects(self, collection_name: str) -> List[str]:
        """Retorna lista de paths de projetos na coleção."""
        return self.collections.get(collection_name, [])

    def get_collection_projects(self, collection_name: str) -> List[str]:
        """Alias para get_projects() (compatibilidade com UI)."""
        return self.get_projects(collection_name)

    def get_project_collections(self, project_path: str) -> List[str]:
        """Retorna lista de coleções que contêm o projeto (ordenada)."""
        return sorted([
            name for name, paths in self.collections.items()
            if project_path in paths
        ])

    def is_project_in_collection(self, collection_name: str, project_path: str) -> bool:
        """Verifica se projeto está em coleção."""
        return project_path in self.collections.get(collection_name, [])

    # === Utilitários ===

    def clean_orphan_projects(self, valid_paths: Set[str]) -> int:
        """
        Remove referências a projetos que não existem mais.

        Returns:
            Número de referências removidas
        """
        removed_count = 0

        for collection_name in self.collections:
            original_size = len(self.collections[collection_name])
            self.collections[collection_name] = [
                path for path in self.collections[collection_name]
                if path in valid_paths
            ]
            removed_count += original_size - len(self.collections[collection_name])

        if removed_count > 0:
            self.save()
            self.logger.info(
                "🧹 %d referências órfãs removidas das coleções",
                removed_count
            )

        return removed_count

    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do sistema de coleções."""
        total_projects = sum(len(paths) for paths in self.collections.values())
        unique_projects = len(set(
            path for paths in self.collections.values() for path in paths
        ))

        return {
            "total_collections": len(self.collections),
            "total_entries": total_projects,
            "unique_projects": unique_projects,
        }
