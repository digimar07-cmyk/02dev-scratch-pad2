# ⚠️ TESTES ARQUIVADOS — 2026-03-13

## Motivo do Arquivamento

Estes testes foram arquivados durante a **Operação Base Limpa** (2026-03-13) como parte
da migração para o plano de desenvolvimento v4.0 baseado na metodologia Akita/XP.

## Problemas que motivaram o arquivamento

- Cobertura real estimada em ~15-20% apesar da existência de arquivos de teste
- Testes incompletos, alguns com apenas estrutura vazia
- Sem cobertura dos módulos mais críticos (main_window, project_modal, controllers)
- Estrutura de conftest sem fixtures reutilizáveis
- Testes não seguiam padrão TDD — foram escritos depois do código
- Ausência de testes de integração funcionais
- Testes estruturais vazios ou sem asserções reais

## O que foi arquivado aqui

```
test_ai_fallbacks.py          — incompleto, sem casos de borda
test_collections_manager.py   — estrutura vazia
test_database.py              — cobertura parcial, sem migração/backup
test_duplicate_detector.py    — parcial
test_name_translator.py       — parcial
test_recursive_scanner.py     — parcial
test_text_utils.py            — parcial
test_thumbnail_cache.py       — estrutura mínima
```

## Referência

Ver `docs/PLANO_DESENVOLVIMENTO_V4.md` para o novo plano completo.
Ver `docs/AKITA_METODOLOGIA.md` para a metodologia que guia o novo ciclo.
