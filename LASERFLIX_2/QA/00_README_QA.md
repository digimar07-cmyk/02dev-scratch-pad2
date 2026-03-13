# LASERFLIX QA — ESTRUTURA ADVERSARIAL v1.0

## FILOSOFIA
- TESTE NÃO EXISTE PARA FAZER O APP PASSAR.
- TESTE EXISTE PARA TENTAR PROVAR QUE O APP ESTÁ ERRADO.
- Verde falso é fracasso.
- Se o relatório final diz REPROVADO, isso é o comportamento correto quando há problemas.

## PROIBIÇÕES ABSOLUTAS
1. Nunca alterar testes após ver falhas para fazer o código passar.
2. Nunca enfraquecer asserts.
3. Nunca adicionar skip/xfail sem justificativa técnica explícita no commit.
4. Nunca alterar thresholds depois de ver o resultado.
5. Nunca considerar "importou sem crash" como prova de funcionamento.
6. Nunca criar smoke tests que capturam toda exceção e dizem que passou.

## SEQUÊNCIA DE EXECUÇÃO
```
01_install_dev_tools.bat     → instala ferramentas
02_run_lint.bat              → ruff + pylint
03_run_types.bat             → basedpyright
04_run_complexity.bat        → radon
05_run_dead_code.bat         → vulture
06_run_duplication.bat       → pylint duplicate-code
07_run_unit_tests.bat        → pytest unit
08_run_integration_tests.bat → pytest integration
09_run_smoke_tests.bat       → pytest smoke + structural
10_run_all.bat               → tudo de uma vez
11_build_consolidated_report.py → gera relatório
12_enforce_quality_gate.py  → APROVADO ou REPROVADO
```

## THRESHOLDS (FIXADOS ANTES DE QUALQUER EXECUÇÃO)
- Complexidade ciclomática máxima por função: **10**
- Tamanho máximo de arquivo: **300 linhas** (conforme FILE_SIZE_LIMIT_RULE.md)
- Cobertura mínima de testes unitários: **40%** (honesto — não inflado)
- Duplicação: máximo **20 blocos** similares
- Ruff errors: **0**
- Type errors (basedpyright): **0**
- Vulture confidence mínima: **80%**

## CLÁUSULA ANTI-MAQUIAGEM
Qualquer redução de falhas deve ser rastreada para:
- diff do código-fonte do APP (não dos testes)
- sem alteração de thresholds
- sem novos arquivos excluídos do escopo
- sem novos skips/xfails

Se a melhora vier dos testes e não do app: REPROVADO automaticamente.

## ARQUIVOS DE RELATÓRIO GERADOS
- `reports/ruff_report.txt` — erros de lint ruff
- `reports/pylint_report.txt` — erros e smells pylint
- `reports/types_report.txt` — erros de tipo basedpyright
- `reports/complexity_cc_report.txt` — complexidade ciclomática por função
- `reports/complexity_mi_report.txt` — índice de manutenibilidade
- `reports/dead_code_report.txt` — símbolos não usados (vulture)
- `reports/duplication_report.txt` — blocos duplicados
- `reports/pytest_unit.xml` — resultado testes unitários
- `reports/pytest_integration.xml` — resultado testes integração
- `reports/pytest_smoke.xml` — resultado smoke + structural
- `reports/CONSOLIDATED_REPORT.txt` — relatório final agregado
- `reports/QUALITY_GATE.txt` — **APROVADO** ou **REPROVADO**

## COMO INTERPRETAR
- `QUALITY_GATE.txt` diz `REPROVADO`: há falha crítica. Veja `CRITICAL_FAILURES`.
- Complexidade CC alta: maior risco de regressão. Refatore antes de adicionar features.
- Vulture lista símbolo como morto: verifique antes de deletar — pode ser callback tkinter.
- Pylint duplicate-code: candidatos a extração obrigatória.
- Basedpyright type errors: contratos quebrados. Não suprima sem explicar.
