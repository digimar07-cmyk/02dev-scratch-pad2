# Estrutura de Testes — Laserflix

## Metodologia (Akita)

Baseado nos princípios extraídos do blog [akitaonrails.com](https://akitaonrails.com/):

### Princípios fundamentais

1. **Testes são especificações de comportamento** — descrevem O QUE o código deve fazer, não COMO.
2. **Red → Green → Refactor** — rodar um teste, ver falhar (Red), consertar o app (Green), refatorar.
3. **Um teste por vez** — nunca pular um teste vermelho correndo para o próximo.
4. **Testes NUNCA são modificados** — o que se corrige é o código do app.
5. **Isolamento total** — nenhum teste usa disco real, DB real ou estado compartilhado.
6. **Nomenclatura expressiva** — `test_dado_estado_quando_acao_entao_resultado`.
7. **AAA: Arrange → Act → Assert** — cada teste segue exatamente esta estrutura.
8. **ZOMBIES**: Zero, One, Many, Boundary, Interface, Exception, Simple scenarios.

---

## Como rodar (um por vez)

```bash
# Instalar dependências
pip install pytest pytest-cov

# Rodar UM teste específico (metodologia Akita: um por vez)
pytest tests/unit/test_database.py::TestDatabaseManager::test_dado_db_vazio_quando_get_project_entao_retorna_none -v

# Rodar TODOS os testes de um módulo
pytest tests/unit/test_database.py -v

# Ver quais testes existem (sem rodar)
pytest tests/ --collect-only

# Rodar com cobertura
pytest tests/ --cov=core --cov=utils --cov-report=term-missing
```

---

## Estrutura

```
tests/
  conftest.py                         # Fixtures compartilhadas
  README_TESTES.md                    # Este arquivo
  unit/
    __init__.py
    test_database.py                  # DatabaseManager (core/database.py)
    test_collections_manager.py       # CollectionsManager (core/collections_manager.py)
    test_text_utils.py                # text_utils (utils/text_utils.py)
    test_duplicate_detector.py        # DuplicateDetector (utils/duplicate_detector.py)
    test_recursive_scanner.py         # RecursiveScanner (utils/recursive_scanner.py)
    test_virtual_scroll_manager.py    # VirtualScrollManager (core/virtual_scroll_manager.py)
  integration/
    __init__.py
    test_database_collections.py      # DB + Collections integrados
    test_scanner_database.py          # Scanner → DB pipeline
```

---

## Ciclo de trabalho

```
1. Escolher UM teste
2. Rodar → RED (falha esperada)
3. Identificar o erro no código do APP
4. Corrigir APENAS o app (nunca o teste)
5. Rodar → GREEN
6. Próximo teste
```

**NUNCA modificar os testes. SEMPRE corrigir o app.**
