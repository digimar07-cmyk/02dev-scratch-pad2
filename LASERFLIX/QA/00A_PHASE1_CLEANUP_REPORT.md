# Fase 1 — Invalidação da base antiga

Esta fase assume que qualquer estrutura anterior de QA/testes/checks pode estar contaminada, enviesada ou maquiada.

## Regras aplicadas
- não herdar automaticamente configs antigas de QA;
- não confiar em relatórios antigos;
- não confiar em testes antigos sem revalidação;
- não usar thresholds herdados por conveniência.

## Diretórios recriados nesta fase
- `QA/`
- `tests/unit/`
- `tests/integration/`
- `tests/smoke/`

## Observação
O código-fonte do app não é modificado por esta reconstrução.
