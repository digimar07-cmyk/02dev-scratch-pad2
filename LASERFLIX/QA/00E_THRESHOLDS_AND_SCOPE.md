# Thresholds e escopo

## Escopo
Inclui:
- `main.py`
- `ai/`
- `config/`
- `core/`
- `ui/`
- `utils/`

Exclui apenas artefatos operacionais:
- `__pycache__/`
- `*.pyc`
- `.coverage`
- `*.log`
- `*.backup*`
- `laserflix_backups/`

## Thresholds iniciais
- Radon CC: alerta acima de B, reprovação a partir de D relevante
- Duplicação: qualquer grupo >= 20 linhas iguais deve ser relatado
- Smoke test: qualquer falha estrutural reprova
- Type errors relevantes: reprovam
- Falhas de importação: reprovam
