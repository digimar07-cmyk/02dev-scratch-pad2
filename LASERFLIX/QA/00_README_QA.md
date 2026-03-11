# QA do LASERFLIX

Esta estrutura foi reconstruída do zero para atuar como auditor independente do código.

## Princípios
- testes existem para encontrar defeitos reais;
- verde falso é fracasso;
- a base de testes não deve ser alterada para esconder defeitos;
- o projeto deve reprovar se houver falhas críticas.

## Ordem de execução
1. `QA\01_install_dev_tools.bat`
2. `QA\10_run_all.bat`

## Execução por etapa
- `QA\02_run_lint.bat`
- `QA\03_run_types.bat`
- `QA\04_run_complexity.bat`
- `QA\05_run_dead_code.bat`
- `QA\06_run_duplication.bat`
- `QA\07_run_unit_tests.bat`
- `QA\08_run_integration_tests.bat`
- `QA\09_run_smoke_tests.bat`

## Saídas
Relatórios ficam em `QA\reports\`.
