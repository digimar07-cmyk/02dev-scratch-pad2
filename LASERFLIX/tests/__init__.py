"""
tests/__init__.py

Permite que pytest encontre os módulos do projeto (core, ui, utils, ai, config).
"""
import sys
import os

# Adiciona diretório raiz do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
