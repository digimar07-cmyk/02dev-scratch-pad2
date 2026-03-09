# Changelog — Laserflix

## [4.0.1.3] - 2026-03-09

### Fixed
- **BRANDT-bugfix**: Restaurados métodos de paginação ausentes no `BaseDisplayController`
  (`next_page`, `prev_page`, `first_page`, `last_page`) que causavam `AttributeError`
  ao final da importação de pastas com análise automática

### Chore (Sprint 1 — Brandt: 100% concluído)
- **BRANDT-04**: Removido `Novo(a) Text Document.txt` (arquivo vazio/lixo)
- Sprint 1 encerrado: todos os 5 itens executáveis concluídos
  (BRANDT-01 a 05 ✅ | BRANDT-06 adiado para Sprint 3B por decisão)

---

## [4.0.1.2] - 2026-03-09

### Changed
- **Estrutura unificada**: Removidos nomes de versão das pastas
- **Controle interno**: Versão agora gerenciada apenas em `VERSION` e `config/settings.py`
- **Testes integrados**: Sprint 0 (Tanaka) — infraestrutura de testes pytest

### Added
- `tests/` com smoke tests básicos para DatabaseManager
- `pytest.ini` com configuração padrão
- `requirements-dev.txt` com dependências de desenvolvimento
- `conftest.py` com fixtures compartilhadas

### Chore (Sprint 1 — Brandt: parcial)
- **BRANDT-01**: Removido `display_controller.py` legado — `OptimizedDisplayController` é o único controller de display
- **BRANDT-02**: Removido `project_management_controller.py` — código morto, zero imports
- **BRANDT-03**: Removido `main_window_pre_selectionctrl.py` — arquivo de backup indevido no repo
- **BRANDT-05**: `modal_manager.py` movido de `/controllers/` para `/managers/` + todos os imports atualizados

---

## [4.0.1.1] - 2026-03-09

### Fixed
- Rollback do Sprint 1 (BRANDT) que quebrou import/display
- Restaurada versão funcional antes das refatorações problemáticas

---

## [4.0.0.9] - 2026-03-08

### Added
- Sistema de performance com 3 otimizações (4.5× faster)
- SelectionController integrado como componente
- Fix de flicker na seleção visual de cards

### Changed
- Refatoração completa de `main_window.py` (orquestrador puro)
- DisplayController extraído para `OptimizedDisplayController`

---

## [4.0.0.8] - 2026-03-01

### Added
- Sistema de coleções/playlists (F-08)
- Filtros empilháveis com chips (F-07)
- Busca bilíngue EN + PT-BR (HOT-14)

---

## [4.0.0.2] - 2026-02-15

### Changed
- **Migração de modelos**: 7 modelos (24.3 GB) → 2 modelos (3.7 GB)
- `qwen3.5:4b` multimodal substituindo todos os anteriores
- Economia de 84.7% em espaço em disco

---

## [3.x] - Legacy

Versões antigas antes da migração de modelos e refatoração MVC.
