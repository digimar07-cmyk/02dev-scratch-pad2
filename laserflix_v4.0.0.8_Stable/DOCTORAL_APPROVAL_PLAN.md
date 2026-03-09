# PLANO DE APROVAÇÃO DOUTORAL — Laserflix v4.0.0.9

> **Objetivo:** Aprovação 100% na Banca Examinadora de Doutorado em Engenharia de Software  
> **Data de criação:** 09/03/2026  
> **Prazo alvo:** 90 dias (deadline: 07/06/2026)  
> **Versão alvo de aprovação:** 4.1.0.0  
> **Status geral:** 🔴 EM EXECUÇÃO

---

## Índice

1. [Painel de Controle Geral](#1-painel-de-controle-geral)
2. [Plano Dr. Brandt — Arquitetura](#2-plano-dr-brandt--arquitetura)
3. [Plano Dra. Tanaka — Qualidade e Testes](#3-plano-dra-tanaka--qualidade-e-testes)
4. [Plano Dr. Volkov — Padrões de Projeto](#4-plano-dr-volkov--padrões-de-projeto)
5. [Plano Dra. Osei — Manutenibilidade](#5-plano-dra-osei--manutenibilidade)
6. [Plano Dr. Mendonça — IHC e Produto](#6-plano-dr-mendonça--ihc-e-produto)
7. [Cronograma Integrado de Sprints](#7-cronograma-integrado-de-sprints)
8. [Critérios de Aceitação por Doutor](#8-critérios-de-aceitação-por-doutor)
9. [Checklist Final de Reapresentação](#9-checklist-final-de-reapresentação)

---

## 1. Painel de Controle Geral

| Doutor | Critério Principal | Status Atual | Meta |
|---|---|:---:|:---:|
| Prof. Dr. Brandt | Arquitetura limpa, sem código morto | 🔴 REPROVADO | ✅ Aprovado |
| Profa. Dra. Tanaka | Cobertura de testes ≥ 60% | 🔴 REPROVADO | ✅ Aprovado |
| Prof. Dr. Volkov | API pública no DB + contratos formais | 🔴 REPROVADO | ✅ Aprovado |
| Profa. Dra. Osei | Type hints + decomposição do __init__ | 🟡 PARCIAL | ✅ Aprovado |
| Prof. Dr. Mendonça | Virtual scroll + feedback correto | 🟡 PARCIAL | ✅ Aprovado |

**Score atual:** 6.6/10 → **Score alvo:** ≥ 9.0/10

---

## 2. Plano Dr. Brandt — Arquitetura

> *"Dois controllers para a mesma função coexistem. Isso não é refatoração — é abandono."*

### Diagnóstico

O Prof. Brandt reprovou por 3 razões específicas:
1. Arquivo legado `display_controller.py` não removido após substituição
2. `modal_manager.py` na pasta `/controllers/` quando deveria estar em `/managers/`
3. Arquivos mortos (`project_management_controller.py`, `main_window_pre_selectionctrl.py`, `virtual_scroll.py` sem uso, `Novo(a) Text Document.txt`)

### Tarefas

#### BRANDT-01 — Remover `display_controller.py` legado

**Risco:** Baixo — confirmar que nenhum arquivo importa `display_controller` antes de remover.

```bash
# ANTES de remover — verificar dependências:
grep -r "display_controller" laserflix_v4.0.0.8_Stable/ --include="*.py"
# Se resultado vazio ou apenas o próprio arquivo → seguro para remover

git rm laserflix_v4.0.0.8_Stable/ui/controllers/display_controller.py
git commit -m "chore(BRANDT-01): remove display_controller.py legado"
```

**Critério de aceite:** `display_controller.py` ausente do repositório. `grep` retorna zero resultados de import.

---

#### BRANDT-02 — Remover `project_management_controller.py` (código morto)

**Risco:** Baixo — verificar imports antes.

```bash
grep -r "project_management_controller" laserflix_v4.0.0.8_Stable/ --include="*.py"
# Se zero resultados → remover

git rm laserflix_v4.0.0.8_Stable/ui/controllers/project_management_controller.py
git commit -m "chore(BRANDT-02): remove project_management_controller.py — código morto"
```

**Critério de aceite:** Arquivo ausente. Zero imports no codebase.

---

#### BRANDT-03 — Remover `main_window_pre_selectionctrl.py` (backup no repo)

**Risco:** Zero — arquivo de 100 bytes, apenas um stub/backup.

```bash
git rm laserflix_v4.0.0.8_Stable/ui/main_window_pre_selectionctrl.py
git commit -m "chore(BRANDT-03): remove arquivo de backup main_window_pre_selectionctrl.py"
```

**Critério de aceite:** Arquivo ausente do repositório.

---

#### BRANDT-04 — Remover `Novo(a) Text Document.txt` (lixo)

**Risco:** Zero.

```bash
git rm "laserflix_v4.0.0.8_Stable/Novo(a) Text Document.txt"
git commit -m "chore(BRANDT-04): remove arquivo vazio de texto"
```

**Critério de aceite:** Arquivo ausente.

---

#### BRANDT-05 — Mover `modal_manager.py` para `/managers/`

**Risco:** Médio — todos os imports do `modal_manager` precisam ser atualizados.

```bash
# Passo 1: verificar quem importa
grep -r "modal_manager" laserflix_v4.0.0.8_Stable/ --include="*.py"

# Passo 2: mover
git mv laserflix_v4.0.0.8_Stable/ui/controllers/modal_manager.py \
        laserflix_v4.0.0.8_Stable/ui/managers/modal_manager.py
```

```python
# Passo 3: em CADA arquivo que importava de controllers/:
# ANTES:
from ui.controllers.modal_manager import ModalManager
# DEPOIS:
from ui.managers.modal_manager import ModalManager
```

```bash
# Passo 4: atualizar __init__.py dos dois pacotes
# ui/controllers/__init__.py — remover ModalManager
# ui/managers/__init__.py — adicionar ModalManager

git add -A
git commit -m "refactor(BRANDT-05): move modal_manager.py de /controllers para /managers"
```

**Critério de aceite:** `modal_manager.py` em `/managers/`. Zero imports da localização antiga.

---

#### BRANDT-06 — Decidir e executar `virtual_scroll.py`

**Decisão a tomar:** Integrar OU remover. Não existe uma terceira opção aceitável.

**Opção A — Remover (mais rápido):**
```bash
git rm laserflix_v4.0.0.8_Stable/ui/virtual_scroll.py
git commit -m "chore(BRANDT-06): remove virtual_scroll.py não integrado"
```

**Opção B — Integrar (mais valor de produto):**
```python
# Em main_window.py — substituir paginação simples:
from ui.virtual_scroll import VirtualScroll

def _setup_core(self) -> None:
    # ...
    self.virtual_scroll = VirtualScroll(
        canvas=self.content_canvas,
        item_height=220,
        render_callback=self._render_card_at_index
    )
```
> ⚠️ **Recomendação:** Opção B — integrar. Valoriza o produto perante o Prof. Mendonça também.

**Critério de aceite:** Arquivo ausente OU integrado e funcionando. Nunca os dois.

---

### Resultado esperado — Brandt

Após execução dos 6 itens:
- Diretório `/controllers/` terá apenas os 4 controllers ativos e corretos
- Diretório `/managers/` terá todos os 7 managers no lugar certo
- Zero arquivos mortos no repositório
- **Score Arquitetura:** 7.5 → 9.5/10

---

## 3. Plano Dra. Tanaka — Qualidade e Testes

> *"Zero testes. Um software sem testes não é um software de doutorado — é um protótipo."*

### Diagnóstico

A Profa. Tanaka reprovou por uma razão simples e inegociável: **zero cobertura de testes**. O bug crítico do `save()` → `save_database()` existiu em produção desde a criação do controller e foi detectado apenas em uso real. Cobertura mínima exigida: **60% em `core/` e `ui/controllers/`**.

### Tarefas

#### TANAKA-01 — Criar estrutura de testes

```bash
# Criar estrutura
mkdir -p laserflix_v4.0.0.8_Stable/tests
touch laserflix_v4.0.0.8_Stable/tests/__init__.py
touch laserflix_v4.0.0.8_Stable/tests/conftest.py

# Instalar dependências
pip install pytest pytest-cov pytest-mock

# Adicionar ao requirements.txt
echo "pytest>=8.0.0" >> requirements.txt
echo "pytest-cov>=5.0.0" >> requirements.txt
echo "pytest-mock>=3.14.0" >> requirements.txt
```

**Critério de aceite:** `tests/` existe, `pytest` executa sem erros.

---

#### TANAKA-02 — `conftest.py` com fixtures compartilhadas

```python
# tests/conftest.py
import pytest
import json
from pathlib import Path
from core.database import DatabaseManager
from core.collections_manager import CollectionsManager


@pytest.fixture
def tmp_db(tmp_path):
    """DatabaseManager com banco de dados temporário vazio."""
    db_file = tmp_path / "test_db.json"
    db = DatabaseManager(str(db_file))
    return db


@pytest.fixture
def tmp_db_with_data(tmp_path):
    """DatabaseManager com 3 projetos pré-carregados."""
    db_file = tmp_path / "test_db.json"
    db = DatabaseManager(str(db_file))
    db.database = {
        "/proj/alpha": {"name": "Alpha", "category": "Motion", "tags": []},
        "/proj/beta":  {"name": "Beta",  "category": "Print",  "tags": ["logo"]},
        "/proj/gamma": {"name": "Gamma", "category": "Motion", "tags": []},
    }
    db.save_database()
    return db


@pytest.fixture
def tmp_collections(tmp_path):
    """CollectionsManager com arquivo temporário."""
    col_file = tmp_path / "collections.json"
    return CollectionsManager(str(col_file))
```

---

#### TANAKA-03 — `test_database.py`

```python
# tests/test_database.py
import pytest
import json
from core.database import DatabaseManager


class TestDatabaseLoad:
    def test_load_empty_db_returns_empty_dict(self, tmp_db):
        tmp_db.load_database()
        assert tmp_db.database == {}

    def test_load_existing_data(self, tmp_db_with_data):
        tmp_db_with_data.load_database()
        assert "/proj/alpha" in tmp_db_with_data.database

    def test_load_corrupted_json_returns_empty(self, tmp_path):
        db_file = tmp_path / "bad.json"
        db_file.write_text("{INVALID JSON")
        db = DatabaseManager(str(db_file))
        db.load_database()
        assert db.database == {}

    def test_load_uses_bak_when_main_corrupted(self, tmp_path):
        db_file = tmp_path / "db.json"
        bak_file = tmp_path / "db.json.bak"
        db_file.write_text("{INVALID")
        bak_file.write_text(json.dumps({"/proj/from_bak": {"name": "FromBak"}}))
        db = DatabaseManager(str(db_file))
        db.load_database()
        assert "/proj/from_bak" in db.database


class TestDatabaseSave:
    def test_save_persists_to_disk(self, tmp_db_with_data, tmp_path):
        tmp_db_with_data.save_database()
        content = json.loads((tmp_path / "test_db.json").read_text())
        assert "/proj/alpha" in content

    def test_save_creates_bak_on_existing_file(self, tmp_db_with_data, tmp_path):
        tmp_db_with_data.save_database()  # primeira vez
        tmp_db_with_data.save_database()  # segunda vez — deve criar .bak
        bak = tmp_path / "test_db.json.bak"
        assert bak.exists()

    def test_atomic_write_no_partial_file(self, tmp_db_with_data, tmp_path):
        tmp_db_with_data.save_database()
        # Arquivo final deve existir, temporário não
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0


class TestDatabaseOperations:
    def test_add_project(self, tmp_db):
        tmp_db.database["/proj/new"] = {"name": "New"}
        assert "/proj/new" in tmp_db.database

    def test_remove_project(self, tmp_db_with_data):
        del tmp_db_with_data.database["/proj/alpha"]
        assert "/proj/alpha" not in tmp_db_with_data.database

    def test_project_count(self, tmp_db_with_data):
        assert len(tmp_db_with_data.database) == 3
```

**Critério de aceite:** `pytest tests/test_database.py -v` passa com 100% dos testes.

---

#### TANAKA-04 — `test_selection_controller.py`

```python
# tests/test_selection_controller.py
import pytest
from unittest.mock import MagicMock, call
from ui.controllers.selection_controller import SelectionController
from core.database import DatabaseManager
from core.collections_manager import CollectionsManager


@pytest.fixture
def ctrl(tmp_db_with_data, tmp_collections):
    c = SelectionController(
        database=tmp_db_with_data.database,
        db_manager=tmp_db_with_data,
        collections_manager=tmp_collections,
    )
    return c


class TestSelectionMode:
    def test_enter_selection_mode(self, ctrl):
        ctrl.toggle_selection_mode()
        assert ctrl.selection_mode is True

    def test_exit_selection_mode(self, ctrl):
        ctrl.toggle_selection_mode()
        ctrl.toggle_selection_mode()
        assert ctrl.selection_mode is False

    def test_on_mode_changed_callback_called(self, ctrl):
        cb = MagicMock()
        ctrl.on_mode_changed = cb
        ctrl.toggle_selection_mode()
        cb.assert_called_once_with(True)


class TestRemoveSelected:
    def test_remove_persists_to_disk(self, ctrl, tmp_db_with_data, tmp_path):
        """BUG REGRESSION: save() não existia — este teste teria capturado."""
        ctrl.selection_mode = True
        ctrl.selected_paths = {"/proj/alpha"}
        ctrl.remove_selected(parent_window=None)
        # Verifica persistência — recarregar do disco
        reloaded = DatabaseManager(str(tmp_path / "test_db.json"))
        reloaded.load_database()
        assert "/proj/alpha" not in reloaded.database

    def test_remove_clears_from_memory(self, ctrl):
        ctrl.selection_mode = True
        ctrl.selected_paths = {"/proj/beta"}
        ctrl.remove_selected(parent_window=None)
        assert "/proj/beta" not in ctrl.database

    def test_remove_calls_refresh_callback(self, ctrl):
        cb = MagicMock()
        ctrl.on_refresh_needed = cb
        ctrl.selection_mode = True
        ctrl.selected_paths = {"/proj/gamma"}
        ctrl.remove_selected(parent_window=None)
        cb.assert_called_once()

    def test_remove_calls_projects_removed_callback(self, ctrl):
        cb = MagicMock()
        ctrl.on_projects_removed = cb
        ctrl.selection_mode = True
        ctrl.selected_paths = {"/proj/alpha", "/proj/beta"}
        ctrl.remove_selected(parent_window=None)
        cb.assert_called_once_with(2)

    def test_remove_multiple_projects(self, ctrl):
        ctrl.selection_mode = True
        ctrl.selected_paths = {"/proj/alpha", "/proj/beta"}
        ctrl.remove_selected(parent_window=None)
        assert "/proj/alpha" not in ctrl.database
        assert "/proj/beta" not in ctrl.database
        assert "/proj/gamma" in ctrl.database  # não tocado

    def test_remove_empty_selection_does_nothing(self, ctrl):
        original_count = len(ctrl.database)
        ctrl.selection_mode = True
        ctrl.selected_paths = set()
        ctrl.remove_selected(parent_window=None)
        assert len(ctrl.database) == original_count
```

**Critério de aceite:** `pytest tests/test_selection_controller.py -v` passa. Inclui **regression test** do bug de 09/03/2026.

---

#### TANAKA-05 — `test_collections_manager.py`

```python
# tests/test_collections_manager.py
import pytest
from core.collections_manager import CollectionsManager


class TestCreateCollection:
    def test_create_returns_id(self, tmp_collections):
        col_id = tmp_collections.create_collection("Minha Coleção")
        assert col_id is not None
        assert isinstance(col_id, str)

    def test_create_persists(self, tmp_collections):
        tmp_collections.create_collection("Logos")
        tmp_collections.save()
        # Recarregar
        reloaded = CollectionsManager(tmp_collections.file_path)
        reloaded.load()
        names = [c["name"] for c in reloaded.collections.values()]
        assert "Logos" in names

    def test_add_collection_alias(self, tmp_collections):
        """add_collection é alias de create_collection."""
        col_id = tmp_collections.add_collection("Test")
        assert col_id is not None


class TestDeleteCollection:
    def test_delete_removes_collection(self, tmp_collections):
        col_id = tmp_collections.create_collection("Para Deletar")
        tmp_collections.delete_collection(col_id)
        assert col_id not in tmp_collections.collections

    def test_delete_nonexistent_does_not_raise(self, tmp_collections):
        tmp_collections.delete_collection("id_inexistente")  # não deve levantar


class TestProjectsInCollection:
    def test_add_project_to_collection(self, tmp_collections):
        col_id = tmp_collections.create_collection("Favoritos")
        tmp_collections.add_project_to_collection("/proj/x", col_id)
        projects = tmp_collections.get_collection_projects(col_id)
        assert "/proj/x" in projects

    def test_remove_project_from_collection(self, tmp_collections):
        col_id = tmp_collections.create_collection("Favoritos")
        tmp_collections.add_project_to_collection("/proj/x", col_id)
        tmp_collections.remove_project_from_collection("/proj/x", col_id)
        projects = tmp_collections.get_collection_projects(col_id)
        assert "/proj/x" not in projects

    def test_clean_orphans_removes_missing_paths(self, tmp_collections):
        col_id = tmp_collections.create_collection("Test")
        tmp_collections.add_project_to_collection("/proj/ghost", col_id)
        existing = {"/proj/real": {}}
        tmp_collections.clean_orphan_projects(existing)
        projects = tmp_collections.get_collection_projects(col_id)
        assert "/proj/ghost" not in projects
```

**Critério de aceite:** `pytest tests/test_collections_manager.py -v` passa com 100%.

---

#### TANAKA-06 — Executar cobertura e atingir ≥ 60%

```bash
# Executar todos os testes com cobertura
pytest tests/ \
  --cov=laserflix_v4.0.0.8_Stable/core \
  --cov=laserflix_v4.0.0.8_Stable/ui/controllers \
  --cov-report=term-missing \
  --cov-report=html:coverage_report \
  --cov-fail-under=60

# Gerar badge de cobertura (opcional mas impressiona a banca)
pip install coverage-badge
coverage-badge -o coverage.svg
```

**Critério de aceite:** Coverage ≥ 60% em `core/` e `ui/controllers/`. `pytest` retorna exit code 0.

---

### Resultado esperado — Tanaka

- 3 arquivos de teste criados (`test_database.py`, `test_selection_controller.py`, `test_collections_manager.py`)
- Regression test permanente para o bug de 09/03/2026
- Coverage ≥ 60% comprovado
- **Score Testabilidade:** 2.0 → 8.5/10

---

## 4. Plano Dr. Volkov — Padrões de Projeto

> *"self.database = self.db_manager.database viola o Princípio de Demeter e o DIP simultaneamente."*

### Diagnóstico

O Prof. Volkov reprovou por 2 problemas de design:
1. Acesso direto ao dict interno do `DatabaseManager` — viola encapsulamento, DIP e Princípio de Demeter
2. Callbacks sem contrato formal — ninguém sabe a assinatura esperada

### Tarefas

#### VOLKOV-01 — API pública no `DatabaseManager`

**Risco:** Médio-alto. Após adicionar a API, deve-se migrar os pontos de acesso direto progressivamente.

**Passo 1 — Adicionar métodos ao `database.py`:**

```python
# core/database.py — ADICIONAR estes métodos à classe DatabaseManager:

def get_project(self, path: str) -> dict | None:
    """Retorna dados de um projeto pelo caminho. None se não encontrado."""
    return self.database.get(path)

def set_project(self, path: str, data: dict) -> None:
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

def all_projects(self) -> dict:
    """Retorna cópia do dicionário completo. Nunca a referência interna."""
    return dict(self.database)

def project_count(self) -> int:
    """Retorna total de projetos."""
    return len(self.database)

def iter_projects(self):
    """Itera sobre (path, data) de todos os projetos."""
    return self.database.items()
```

**Passo 2 — Migrar `selection_controller.py`:**

```python
# ANTES:
del self.database[path]
# DEPOIS:
self.db_manager.remove_project(path)
```

**Passo 3 — Migrar demais acessos diretos ao dict:**

```bash
# Localizar todos os acessos diretos ao database interno:
grep -rn "\.database\[" laserflix_v4.0.0.8_Stable/ --include="*.py" | grep -v "test_"
grep -rn "self\.database =" laserflix_v4.0.0.8_Stable/ --include="*.py" | grep -v "database\.py"
```

Para cada resultado encontrado, substituir pelo método correspondente da API.

**Critério de aceite:** Zero ocorrências de `self.database[` fora de `database.py`. Zero `self.database =` fora do próprio `DatabaseManager`.

---

#### VOLKOV-02 — Contratos formais para callbacks (Protocol)

**Risco:** Baixo — mudança apenas de tipagem, sem alterar comportamento.

```python
# Criar: core/protocols.py
"""
Protocolos formais para contratos de callback entre controllers e views.
Substitui o padrão informal 'if self.on_xxx: self.on_xxx()' sem tipagem.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class RefreshCallback(Protocol):
    """Callback chamado quando a tela precisa ser atualizada."""
    def __call__(self) -> None: ...


@runtime_checkable
class ModeChangedCallback(Protocol):
    """Callback chamado quando o modo de seleção muda."""
    def __call__(self, is_active: bool) -> None: ...


@runtime_checkable
class ProjectsRemovedCallback(Protocol):
    """Callback chamado após remoção de projetos."""
    def __call__(self, count: int) -> None: ...


@runtime_checkable
class ProgressCallback(Protocol):
    """Callback de progresso para operações longas."""
    def __call__(self, current: int, total: int, message: str) -> None: ...


@runtime_checkable
class DisplayUpdatedCallback(Protocol):
    """Callback após atualização do display."""
    def __call__(self, project_count: int) -> None: ...
```

```python
# Aplicar em selection_controller.py:
from typing import Optional
from core.protocols import (
    RefreshCallback,
    ModeChangedCallback,
    ProjectsRemovedCallback,
)

class SelectionController:
    def __init__(self, ...) -> None:
        self.on_refresh_needed: Optional[RefreshCallback] = None
        self.on_mode_changed: Optional[ModeChangedCallback] = None
        self.on_projects_removed: Optional[ProjectsRemovedCallback] = None
```

**Critério de aceite:** `core/protocols.py` existe. Todos os controllers usam `Optional[XxxCallback]` nos atributos de callback. `mypy` não reporta erros nos controllers.

---

#### VOLKOV-03 — Verificar Strategy pattern no sistema de fallbacks

O Prof. Volkov aprovou este ponto, mas exige documentação explícita do padrão:

```python
# ai/fallbacks.py — ADICIONAR docstring de padrão se ausente:
"""
Implementa o padrão Strategy para análise de IA com fallback gracioso.

Estrutura:
  AnalysisStrategy (Protocol)
    ├── OllamaAnalysisStrategy    — usa Ollama quando online
    └── FallbackAnalysisStrategy  — usa heurísticas locais quando offline

O OllamaClient seleciona a estratégia automaticamente via health check.
"""
```

**Critério de aceite:** Docstring de padrão presente. `grep "Strategy" ai/fallbacks.py` retorna resultado.

---

### Resultado esperado — Volkov

- `DatabaseManager` com API completa de 8 métodos públicos
- `core/protocols.py` com 5 Protocols formais
- Zero acessos diretos ao dict interno fora de `database.py`
- **Score Acoplamento:** 6.5 → 9.0/10

---

## 5. Plano Dra. Osei — Manutenibilidade

> *"Zero type hints em 2026 é inaceitável. mypy teria capturado o bug save() automaticamente."*

### Diagnóstico

A Profa. Osei aprovou parcialmente. Dois problemas:
1. Ausência de type hints em todos os arquivos
2. `__init__` do `main_window.py` com 280 linhas — Constructor Overload Syndrome
3. Imports locais dentro de métodos (import circular latente)

### Tarefas

#### OSEI-01 — Configurar `mypy` e `ruff`

```bash
pip install mypy ruff

# Criar mypy.ini na raiz do projeto:
cat > laserflix_v4.0.0.8_Stable/mypy.ini << 'EOF'
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True
check_untyped_defs = True

[mypy-tkinter.*]
ignore_missing_imports = True

[mypy-PIL.*]
ignore_missing_imports = True
EOF

# Criar ruff.toml:
cat > laserflix_v4.0.0.8_Stable/ruff.toml << 'EOF'
[tool.ruff]
python-version = "3.10"
select = ["E", "F", "I", "ANN"]
ignore = ["ANN101", "ANN102"]
EOF
```

**Critério de aceite:** `mypy core/ ui/controllers/` executa sem erros após aplicação dos type hints.

---

#### OSEI-02 — Type hints em `core/database.py`

```python
# core/database.py — HEADER com imports de tipagem
from __future__ import annotations
from typing import Any, Iterator
import os
import json
import logging
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_file: str | Path) -> None:
        self.db_file: Path = Path(db_file)
        self.database: dict[str, dict[str, Any]] = {}
        self.logger: logging.Logger = logging.getLogger(__name__)

    def load_database(self) -> bool:
        """Carrega o banco de dados do disco. Retorna True se bem-sucedido."""
        ...

    def save_database(self) -> bool:
        """Salva atomicamente o banco. Retorna True se bem-sucedido."""
        ...

    def get_project(self, path: str) -> dict[str, Any] | None: ...
    def set_project(self, path: str, data: dict[str, Any]) -> None: ...
    def remove_project(self, path: str) -> bool: ...
    def has_project(self, path: str) -> bool: ...
    def all_paths(self) -> list[str]: ...
    def all_projects(self) -> dict[str, dict[str, Any]]: ...
    def project_count(self) -> int: ...
    def iter_projects(self) -> Iterator[tuple[str, dict[str, Any]]]: ...
```

---

#### OSEI-03 — Type hints em `core/collections_manager.py`

```python
# core/collections_manager.py
from __future__ import annotations
from typing import Any


class CollectionsManager:
    def __init__(self, col_file: str) -> None:
        self.file_path: str = col_file
        self.collections: dict[str, dict[str, Any]] = {}

    def create_collection(self, name: str) -> str: ...
    def add_collection(self, name: str) -> str: ...  # alias
    def delete_collection(self, col_id: str) -> None: ...
    def get_collection(self, col_id: str) -> dict[str, Any] | None: ...
    def add_project_to_collection(self, path: str, col_id: str) -> None: ...
    def remove_project_from_collection(self, path: str, col_id: str) -> None: ...
    def get_collection_projects(self, col_id: str) -> list[str]: ...
    def clean_orphan_projects(self, existing_paths: dict[str, Any]) -> int: ...
    def get_stats(self) -> dict[str, int]: ...
    def save(self) -> None: ...
    def load(self) -> None: ...
```

---

#### OSEI-04 — Type hints em todos os `ui/controllers/`

```python
# ui/controllers/selection_controller.py — EXEMPLO COMPLETO
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tkinter as tk

if TYPE_CHECKING:
    from core.database import DatabaseManager
    from core.collections_manager import CollectionsManager

from core.protocols import (
    RefreshCallback, ModeChangedCallback, ProjectsRemovedCallback
)


class SelectionController:
    def __init__(
        self,
        database: dict,
        db_manager: DatabaseManager,
        collections_manager: CollectionsManager,
    ) -> None:
        self.database = database
        self.db_manager = db_manager
        self.collections_manager = collections_manager
        self.selection_mode: bool = False
        self.selected_paths: set[str] = set()
        self.on_refresh_needed: Optional[RefreshCallback] = None
        self.on_mode_changed: Optional[ModeChangedCallback] = None
        self.on_projects_removed: Optional[ProjectsRemovedCallback] = None

    def toggle_selection_mode(self) -> None: ...
    def toggle_project_selection(self, path: str) -> None: ...
    def select_all(self) -> None: ...
    def clear_selection(self) -> None: ...
    def remove_selected(self, parent_window: tk.Misc | None) -> None: ...
    def get_selected_count(self) -> int: ...
    def is_selected(self, path: str) -> bool: ...
```

> Aplicar o mesmo padrão em `analysis_controller.py`, `display_controller.py`, `collection_controller.py`.

**Critério de aceite:** `mypy ui/controllers/ --ignore-missing-imports` sem erros de tipo.

---

#### OSEI-05 — Decomposição do `__init__` do `main_window.py`

Esta é a maior refatoração estrutural. Deve ser feita com cuidado cirúrgico.

**Estratégia:** Extrair seções do `__init__` para métodos privados nomeados, sem alterar lógica.

```python
# ui/main_window.py — ESTRUTURA ALVO
class LaserflixMainWindow:
    """
    Janela principal do Laserflix.
    Orquestrador central (padrão Mediator) — conecta todos os
    controllers, managers e widgets via callbacks.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._init_state()
        self._setup_core()
        self._setup_controllers()
        self._build_ui()
        self._setup_callbacks()
        self._setup_managers()
        self._startup()

    # ── Estado ────────────────────────────────────────────────
    def _init_state(self) -> None:
        """Inicializa variáveis de estado da janela."""
        self._current_filter: str = "all"
        self._current_sort: str = "name"
        self._current_page: int = 0
        self._filter_cache: dict = {}

    # ── Core ──────────────────────────────────────────────────
    def _setup_core(self) -> None:
        """Instancia DatabaseManager, CollectionsManager e AI stack."""
        from core.database import DatabaseManager
        from core.collections_manager import CollectionsManager
        self.db_manager = DatabaseManager()
        self.db_manager.load_database()
        self.database = self.db_manager.database  # TODO: migrar para API
        self.collections_manager = CollectionsManager()
        self.collections_manager.load()

    # ── Controllers ───────────────────────────────────────────
    def _setup_controllers(self) -> None:
        """Instancia todos os controllers MVC."""
        from ui.controllers.selection_controller import SelectionController
        from ui.controllers.analysis_controller import AnalysisController
        from ui.controllers.optimized_display_controller import OptimizedDisplayController
        from ui.controllers.collection_controller import CollectionController
        self.selection_ctrl = SelectionController(...)
        self.display_ctrl = OptimizedDisplayController(...)
        self.analysis_ctrl = AnalysisController(...)
        self.collection_ctrl = CollectionController(...)

    # ── UI ────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        """Constrói todos os widgets via builders."""
        self._build_root_layout()
        self._build_sidebar()
        self._build_header()
        self._build_content_area()
        self._build_selection_bar()
        self._build_status_bar()

    # ── Callbacks ─────────────────────────────────────────────
    def _setup_callbacks(self) -> None:
        """Conecta todos os callbacks entre controllers e widgets."""
        self.selection_ctrl.on_refresh_needed = self._refresh_all
        self.selection_ctrl.on_mode_changed = self._on_selection_mode_changed
        self.selection_ctrl.on_projects_removed = self._on_projects_removed
        self.display_ctrl.on_display_updated = self._on_display_updated
        self.analysis_ctrl.on_progress = self._on_analysis_progress
        self.analysis_ctrl.on_complete = self._on_analysis_complete

    # ── Managers ──────────────────────────────────────────────
    def _setup_managers(self) -> None:
        """Inicializa managers de dialog, toggle, backup, etc."""
        from ui.managers.dialog_manager import DialogManager
        from ui.managers.toggle_manager import ToggleManager
        self.dialog_mgr = DialogManager(self.root, self.db_manager)
        self.toggle_mgr = ToggleManager()

    # ── Startup ───────────────────────────────────────────────
    def _startup(self) -> None:
        """Carrega dados iniciais, exibe primeira tela, agenda tarefas."""
        self._refresh_all()
        self._schedule_auto_backup()
```

**Critério de aceite:** `__init__` com ≤ 15 linhas. Cada `_setup_*` com ≤ 50 linhas. Funcionalidade 100% preservada.

---

#### OSEI-06 — Resolver imports circulares

**Identificar todos os imports locais:**
```bash
grep -rn "^    from " laserflix_v4.0.0.8_Stable/ --include="*.py"
grep -rn "^    import " laserflix_v4.0.0.8_Stable/ --include="*.py"
```

**Solução para cada caso — usar TYPE_CHECKING:**
```python
# No topo do arquivo com import circular:
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.builders.header_builder import HeaderBuilder
    from ui.builders.cards_grid_builder import CardsGridBuilder
    # Estes imports só existem em tempo de checagem de tipo,
    # não em tempo de execução — quebra o ciclo sem mudar comportamento
```

**Critério de aceite:** Zero imports de módulos locais dentro de funções/métodos.

---

### Resultado esperado — Osei

- `mypy` + `ruff` configurados e passando
- Type hints em todos os arquivos de `core/` e `ui/controllers/`
- `__init__` do `main_window.py` com ≤ 15 linhas
- Zero imports locais dentro de métodos
- **Score Qualidade de Código:** 6.0 → 9.0/10
- **Score Manutenibilidade:** 6.0 → 8.5/10

---

## 6. Plano Dr. Mendonça — IHC e Produto

> *"O app mentia. Cards sumiam na tela mas voltavam ao reiniciar. Isso é feedback falso."*

### Diagnóstico

O Prof. Mendonça aprovou o produto mas reprovou como tese por 3 problemas:
1. Feedback falso (bug de 09/03/2026 — já corrigido, mas precisa de teste de regressão)
2. `virtual_scroll.py` existente e não integrado
3. `recursive_import_integration.py` com responsabilidades acumuladas

### Tarefas

#### MENDONCA-01 — Confirmar e documentar correção do feedback falso

O bug foi corrigido em 09/03/2026 (ver CHANGELOG v4.0.0.9). A tarefa aqui é **garantir que nunca volte** via teste de regressão (já coberto no TANAKA-04) e adicionar feedback visual explícito.

```python
# Em selection_controller.py — após remoção bem-sucedida,
# garantir feedback visual ao usuário:
def remove_selected(self, parent_window: tk.Misc | None) -> None:
    if not self.selected_paths:
        return
    count = len(self.selected_paths)
    # ... remoção ...
    self.db_manager.save_database()  # persiste no disco ✅
    self.collections_manager.save()  # remove das coleções ✅
    if self.on_projects_removed:
        self.on_projects_removed(count)  # atualiza status bar ✅
    if self.on_refresh_needed:
        self.on_refresh_needed()  # atualiza tela + sidebar ✅
    # Feedback visual explícito:
    if parent_window and count > 0:
        msg = f"{count} projeto{'s' if count > 1 else ''} removido{'s' if count > 1 else ''}"
        parent_window.after(100, lambda: _show_toast(parent_window, msg))
```

**Critério de aceite:** Teste de regressão passa. Status bar atualiza imediatamente após remoção. Sidebar atualiza contadores.

---

#### MENDONCA-02 — Integrar `virtual_scroll.py`

Esta é a tarefa de maior impacto de produto. O scroll virtual elimina a paginação e torna a navegação fluida.

**Passo 1 — Analisar `virtual_scroll.py` atual:**
```bash
cat laserflix_v4.0.0.8_Stable/ui/virtual_scroll.py
# Identificar: interface esperada, parâmetros, callbacks
```

**Passo 2 — Integrar em `main_window.py`:**
```python
# Em _build_content_area() do main_window.py:
from ui.virtual_scroll import VirtualScroll

self.virtual_scroll = VirtualScroll(
    container=self.content_frame,
    item_height=240,          # altura do ProjectCard
    items_per_row=4,          # colunas do grid
    render_callback=self._render_card,
    total_items_callback=lambda: len(self._get_filtered_projects()),
)
```

**Passo 3 — Adaptar `display_projects()` para usar VirtualScroll:**
```python
def display_projects(self) -> None:
    projects = self._get_filtered_projects()
    if hasattr(self, 'virtual_scroll'):
        self.virtual_scroll.set_items(projects)
        self.virtual_scroll.refresh()
    else:
        self._display_projects_paginated(projects)  # fallback
```

**Critério de aceite:** VirtualScroll renderiza cards sem paginação. `virtual_scroll.py` marcado como INTEGRADO no CHANGELOG.

---

#### MENDONCA-03 — Refatorar `recursive_import_integration.py`

**Identificar responsabilidades no arquivo (20.365 bytes):**
```bash
grep -n "def " laserflix_v4.0.0.8_Stable/ui/recursive_import_integration.py
```

**Extrair para arquivos menores:**
```
recursive_import_integration.py (orquestrador)
  ├── import_scanner.py        — lógica de scan recursivo do sistema de arquivos
  ├── import_progress_dialog.py — UI do diálogo de progresso
  └── import_ai_processor.py   — processamento IA durante importação
```

Cada arquivo resultante deve ter ≤ 200 linhas.

**Critério de aceite:** `recursive_import_integration.py` com ≤ 8 KB. Funcionalidade 100% preservada.

---

#### MENDONCA-04 — Validar heurísticas de Nielsen

O Prof. Mendonça citou violação das heurísticas de Nielsen. Verificar e corrigir:

| Heurística | Problema Identificado | Solução |
|---|---|---|
| **1. Visibilidade do status** | Status bar não atualizava após remoção | ✅ Corrigido em v4.0.0.9 |
| **1. Visibilidade do status** | Análise IA sem indicador de progresso claro | Verificar AnalysisController progress callback |
| **3. Controle do usuário** | Não há "desfazer" após remoção de projetos | Implementar Undo com buffer de 30s (futuro) |
| **9. Ajuda ao diagnóstico** | Erros de Ollama offline não são claros ao usuário | Verificar mensagem de fallback |

**Critério de aceite mínimo:** Items 1 e 9 verificados e funcionando. Item 3 documentado como backlog.

---

### Resultado esperado — Mendonça

- Feedback visual garantido e testado após remoção
- VirtualScroll integrado (ou documentação clara de por que não integrar)
- `recursive_import_integration.py` refatorado em 3 arquivos menores
- **Score Performance:** 7.5 → 9.0/10
- **Score IHC:** implicitamente aprovado

---

## 7. Cronograma Integrado de Sprints

```
SEMANA 1 (09/03 - 15/03) — SPRINT 1: LIMPEZA
├── BRANDT-01  Remover display_controller.py legado
├── BRANDT-02  Remover project_management_controller.py
├── BRANDT-03  Remover main_window_pre_selectionctrl.py
├── BRANDT-04  Remover Novo(a) Text Document.txt
├── BRANDT-05  Mover modal_manager.py para /managers/
└── BRANDT-06  Decisão e execução do virtual_scroll.py

SEMANA 2 (16/03 - 22/03) — SPRINT 2A: FUNDAÇÃO DE QUALIDADE
├── TANAKA-01  Criar estrutura tests/ + conftest.py
├── TANAKA-02  conftest.py com fixtures
├── VOLKOV-01  API pública no DatabaseManager (8 métodos)
└── VOLKOV-02  Criar core/protocols.py com 5 Protocols

SEMANA 3 (23/03 - 29/03) — SPRINT 2B: TESTES E TIPAGEM
├── TANAKA-03  test_database.py (12 testes)
├── TANAKA-04  test_selection_controller.py (9 testes)
├── TANAKA-05  test_collections_manager.py (8 testes)
├── OSEI-01    Configurar mypy + ruff
├── OSEI-02    Type hints em database.py
└── OSEI-03    Type hints em collections_manager.py

SEMANA 4 (30/03 - 05/04) — SPRINT 2C: TYPE HINTS NOS CONTROLLERS
├── OSEI-04    Type hints em selection_controller.py
├── OSEI-04    Type hints em analysis_controller.py
├── OSEI-04    Type hints em optimized_display_controller.py
├── OSEI-04    Type hints em collection_controller.py
├── TANAKA-06  Executar coverage ≥ 60%
└── VOLKOV-03  Documentar Strategy pattern em fallbacks.py

SEMANA 5 (06/04 - 12/04) — SPRINT 3A: REFATORAÇÃO ESTRUTURAL
├── OSEI-05    Decomposição do __init__ (main_window.py)
├── OSEI-06    Resolver imports circulares
└── MENDONCA-01 Confirmar + testar feedback visual pós-remoção

SEMANA 6 (13/04 - 19/04) — SPRINT 3B: PRODUTO
├── MENDONCA-02 Integrar VirtualScroll
└── MENDONCA-04 Validar heurísticas de Nielsen

SEMANA 7 (20/04 - 26/04) — SPRINT 3C: REFATORAÇÃO IMPORT
└── MENDONCA-03 Refatorar recursive_import_integration.py

SEMANA 8-10 (27/04 - 17/05) — SPRINT 4: INTEGRAÇÃO E TESTES FINAIS
├── Executar mypy sem erros
├── pytest com coverage ≥ 60%
├── Smoke test completo do app
├── Atualizar CHANGELOG + VERSION para 4.1.0.0
└── Atualizar TECH_AUDIT.md com scores finais

SEMANA 11-12 (18/05 - 31/05) — BUFFER E DOCUMENTAÇÃO
├── Documentar decisões arquiteturais
├── Atualizar README com nova estrutura
└── Preparar reapresentação para banca

DEADLINE: 07/06/2026 — Reapresentação à banca
```

---

## 8. Critérios de Aceitação por Doutor

### Prof. Dr. Brandt — Arquitetura ✅ quando:
- [ ] Zero arquivos legados em `/controllers/` (`display_controller.py` ausente)
- [ ] Zero código morto (nenhum arquivo sem import no projeto inteiro)
- [ ] `modal_manager.py` em `/managers/`
- [ ] `virtual_scroll.py` integrado OU ausente
- [ ] `main_window_pre_selectionctrl.py` ausente
- [ ] `grep -r "display_controller" . --include="*.py"` retorna zero

### Profa. Dra. Tanaka — Testes ✅ quando:
- [ ] `tests/` existe com `conftest.py`, `test_database.py`, `test_selection_controller.py`, `test_collections_manager.py`
- [ ] `pytest tests/ -v` passa com 100% dos testes
- [ ] `pytest --cov=core --cov=ui/controllers --cov-fail-under=60` retorna exit 0
- [ ] Regression test `test_remove_persists_to_disk` existe e passa
- [ ] `requirements.txt` inclui `pytest` e `pytest-cov`

### Prof. Dr. Volkov — Padrões ✅ quando:
- [ ] `DatabaseManager` tem: `get_project()`, `set_project()`, `remove_project()`, `has_project()`, `all_paths()`, `all_projects()`, `project_count()`, `iter_projects()`
- [ ] `core/protocols.py` existe com ≥ 4 Protocol classes
- [ ] `grep -rn "\.database\[" . --include="*.py" | grep -v database.py` retorna zero
- [ ] Todos os controllers usam `Optional[XxxCallback]` tipado nos atributos de callback
- [ ] `mypy core/ --ignore-missing-imports` sem erros

### Profa. Dra. Osei — Manutenibilidade ✅ quando:
- [ ] `mypy.ini` ou `pyproject.toml` com configuração mypy presente
- [ ] `mypy core/ ui/controllers/ --ignore-missing-imports` retorna zero erros
- [ ] `main_window.__init__` com ≤ 15 linhas
- [ ] Métodos `_setup_core()`, `_setup_controllers()`, `_build_ui()`, `_setup_callbacks()`, `_setup_managers()`, `_startup()` existem no `main_window.py`
- [ ] Zero imports locais dentro de funções/métodos (`grep -n "^    from " **/*.py` retorna zero)
- [ ] `ruff check . --select ANN` sem erros críticos

### Prof. Dr. Mendonça — IHC e Produto ✅ quando:
- [ ] Após remoção: cards desaparecem imediatamente da tela
- [ ] Após remoção: sidebar atualiza contadores imediatamente
- [ ] Após remoção: reiniciar o app não traz de volta os projetos removidos
- [ ] Teste de regressão `test_remove_persists_to_disk` passa
- [ ] VirtualScroll integrado OU `virtual_scroll.py` removido com decisão documentada
- [ ] `recursive_import_integration.py` com ≤ 8 KB

---

## 9. Checklist Final de Reapresentação

> Executar esta checklist na íntegra antes de contatar a banca para reapresentação.

### Verificações Automáticas

```bash
# 1. Sem código morto
grep -r "display_controller" . --include="*.py"        # deve retornar ZERO
grep -r "project_management_controller" . --include="*.py"  # deve retornar ZERO
ls ui/controllers/modal_manager.py 2>/dev/null && echo "FALHOU" || echo "OK"
ls ui/managers/modal_manager.py    2>/dev/null && echo "OK" || echo "FALHOU"

# 2. Testes
pytest tests/ -v --tb=short                            # deve passar 100%
pytest tests/ --cov=core --cov=ui/controllers --cov-fail-under=60  # exit 0

# 3. Tipagem
mypy core/ ui/controllers/ --ignore-missing-imports    # deve retornar: Success

# 4. Linting
ruff check core/ ui/controllers/ --select E,F          # zero erros E/F

# 5. Estrutura do main_window.__init__
python -c "
import ast, sys
tree = ast.parse(open('ui/main_window.py').read())
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                lines = item.end_lineno - item.lineno
                print(f'__init__ tem {lines} linhas')
                if lines > 20:
                    print('FALHOU — mais de 20 linhas')
                    sys.exit(1)
                else:
                    print('OK')
"
```

### Verificações Manuais

- [ ] Iniciar app com `python main.py` — abre sem erros
- [ ] Adicionar 3 projetos via importação manual
- [ ] Selecionar 2 projetos e remover — verificar que desaparecem imediatamente
- [ ] Reiniciar app — projetos removidos NÃO aparecem
- [ ] Sidebar mostra contadores corretos
- [ ] Análise IA funciona (com Ollama) ou mostra fallback correto (sem Ollama)
- [ ] `pytest tests/ -v` — todos os testes verdes
- [ ] `mypy core/ ui/controllers/` — Success
- [ ] `VERSION` = `4.1.0.0`
- [ ] `CHANGELOG.md` atualizado com todas as mudanças
- [ ] `TECH_AUDIT.md` atualizado com scores finais

---

## Histórico deste Documento

| Versão | Data | Evento |
|---|---|---|
| 1.0.0 | 09/03/2026 | Criação — plano de aprovação doutoral completo por avaliador |

---

> *"O problema não é falta de habilidade — é falta de disciplina para fechar o que abre e provar o que afirma."*  
> — Banca Examinadora, 09/03/2026

> *Documento gerado por Perplexity AI (Claude Sonnet 4.6)*
