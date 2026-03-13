"""
utils/duplicate_detector.py - Detector de Duplicatas PRECISO
"""
import os
import re
from collections import defaultdict
from typing import Dict, List
from utils.logging_setup import LOGGER


class DuplicateDetector:
    """Detector de duplicatas baseado em NOME COMPLETO da pasta."""

    def __init__(self):
        self.logger = LOGGER

    def normalize_folder_name(self, folder_name: str) -> str:
        normalized = folder_name.lower()
        normalized = normalized.replace("-", " ").replace("_", " ")
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized.strip()

    def find_duplicates(self, database: Dict[str, dict]) -> Dict[str, List[str]]:
        groups: Dict[str, List[str]] = defaultdict(list)
        for path in database.keys():
            folder_name = os.path.basename(path)
            normalized = self.normalize_folder_name(folder_name)
            groups[normalized].append(path)
        duplicates = {
            norm_name: paths
            for norm_name, paths in groups.items()
            if len(paths) >= 2
        }
        self.logger.info(
            f"🔍 Duplicatas encontradas: {len(duplicates)} grupos, "
            f"{sum(len(paths) for paths in duplicates.values())} projetos afetados"
        )
        return duplicates

    def is_duplicate(self, path1: str, path2: str) -> bool:
        name1 = os.path.basename(path1)
        name2 = os.path.basename(path2)
        return self.normalize_folder_name(name1) == self.normalize_folder_name(name2)

    def get_duplicate_summary(self, database: Dict[str, dict]) -> dict:
        duplicates = self.find_duplicates(database)
        total_duplicates = sum(len(paths) for paths in duplicates.values())
        examples = [
            {
                "normalized_name": norm_name,
                "count": len(paths),
                "paths": [os.path.basename(p) for p in paths],
            }
            for norm_name, paths in list(duplicates.items())[:5]
        ]
        return {
            "total_projects": len(database),
            "duplicate_groups": len(duplicates),
            "duplicate_count": total_duplicates,
            "examples": examples,
        }
