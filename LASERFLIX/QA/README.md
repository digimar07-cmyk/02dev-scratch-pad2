# 🧪 LASERFLIX — Suite de QA

Pasta com todos os scripts de qualidade de código. Execute na ordem numérica.

## Estrutura

```
QA/
├── 00_RODAR_TUDO.bat          ← Executa toda a suite de uma vez
├── 01_ruff_check.bat          ← Análise estática (só lê, não muda nada)
├── 02_ruff_fix.bat            ← Corrige erros automáticos
├── 03_mypy_check.bat          ← Verifica tipos (str, int, dict...)
├── 04_pylint_check.bat        ← Análise profunda de qualidade
├── 05_code_smell_check.bat    ← Score geral ruff+radon+vulture
├── 05_code_smell_check.py     ← Script Python do code smell
├── 06_pytest_run.bat          ← Roda todos os testes unitários
└── reports/                   ← Relatórios gerados automaticamente
```

## O que cada ferramenta detecta

| # | Ferramenta | Tipo | O que detecta |
|---|---|---|---|
| 01 | **Ruff** | Estática | Smells, imports errados, bugs óbvios, estilo |
| 02 | **Ruff Fix** | Estática | Corrige automaticamente o que for possível |
| 03 | **MyPy** | Tipos | Função espera `str`, recebe `int`? MyPy pega |
| 04 | **Pylint** | Qualidade | Score 0-10, funções complexas, acoplamento |
| 05 | **Code Smell** | Score geral | ruff + radon (CC) + vulture (dead code) |
| 06 | **PyTest** | Unitários | Testa se cada função retorna o que deveria |

## Sequência recomendada

1. Rode `00_RODAR_TUDO.bat` para gerar todos os relatórios
2. Envie os arquivos da pasta `reports/` para análise
3. Corrija os problemas encontrados
4. Rode novamente para confirmar as correções

## Relatórios gerados

Todos os relatórios ficam em `QA/reports/` com nome e timestamp.
Após rodar, faça **git add + commit + push** e compartilhe os relatórios.
