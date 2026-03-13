# Contexto de Continuidade — Para Nova Conversa

> **LEIA ESTE ARQUIVO PRIMEIRO ao iniciar qualquer sessão sobre o Laserflix.**
> Contém todo o contexto necessário para retomar o desenvolvimento sem perda de estado.

---

## O Projeto

**Nome:** Laserflix v3.3 → v4.0 em desenvolvimento  
**Tipo:** Aplicação desktop Python (Tkinter/CustomTkinter) para catalogar mídia  
**Repo:** `digimar07-cmyk/dev-scratch-pad2` → pasta `LASERFLIX_2/`  
**Branch:** `main`

### Stack técnica:
- Python + Tkinter (UI)
- JSON → migrando para SQLite (dados)
- Ollama + modelos locais (IA)
- pytest + coverage (testes)
- Windows como plataforma alvo

---

## Arquivos de Referência Fundamentais

```
docs/AKITA_METODOLOGIA.md         ← regras que governam TODO o desenvolvimento
docs/PLANO_DESENVOLVIMENTO_V4.md  ← plano completo com status atualizado ← LER AQUI
docs/CONTEXTO_CONTINUIDADE.md     ← este arquivo
```

**Para saber ONDE estamos:** abrir `PLANO_DESENVOLVIMENTO_V4.md` e ver a seção
"Status de Execução".

---

## Instrução para o AI em Nova Conversa

Quando o usuário iniciar nova conversa, o AI deve:

1. **Ler** `LASERFLIX_2/docs/PLANO_DESENVOLVIMENTO_V4.md` via MCP GitHub
2. **Identificar** qual fase está com status ⏳ (em andamento)
3. **Identificar** a primeira tarefa com `[ ]` (não concluída) nessa fase
4. **Reportar** ao usuário: "Estamos na Fase X, próxima tarefa é Y"
5. **Aguardar** aprovação antes de executar

---

## Estado Atual (2026-03-13)

### O que foi feito nesta sessão:

1. **Análise técnica completa** do app — parecer 7.2/10
   - Ponto forte: `database.py` (qualidade profissional)
   - Ponto forte: `main_window.py` (orquestrador puro)
   - Ponto forte: `project_card.py` (bem organizado)
   - Problema crítico: JSON não escala
   - Problema crítico: cobertura ~15-20%
   - Problema crítico: `recursive_import_integration.py` 20KB

2. **Plano detalhado criado** com 6 fases + pré-fase
   - Baseado na metodologia Akita/XP
   - TDD como processo obrigatório
   - Migração SQLite via Strangler Fig

3. **Operação Base Limpa executada:**
   - Testes antigos arquivados em `tests/_archived/`
   - Docs obsoletos em `docs/archive/`
   - Nova estrutura de testes criada (zerada, limpa)
   - `pytest.ini` configurado
   - `.gitignore` atualizado
   - `conftest.py` reescrito

### Próxima ação:

```
⏳ FASE 0 — Fundação de Segurança
Próxima tarefa: 0.1 — Usuário faz git pull e roda pytest
Expected output: 0 tests collected (ou apenas smoke)
Se OK: AI cria os smoke tests (0.2)
```

---

## Decisões Técnicas Tomadas

| Decisão | Motivo | Fase |
|---------|--------|------|
| SQLite via Strangler Fig | Mesma API, zero risco de regressão | Fase 3 |
| `_on_close()` + WM_DELETE_WINDOW | `__del__` é não-determinístico em Python | Fase 1 |
| CardCallbacks dataclass | Dict com 17 entradas não tem segurança de tipo | Fase 4 |
| Imports no topo (não dentro de método) | Esconde dependência circular | Fase 1 |
| Logging `%s` não f-string | f-string avalia mesmo com log desativado | Fase 1 |
| Testes arquivados, não deletados | Preservação histórica + possível referência | Pré-Fase 0 |

---

## Estrutura de Testes Atual (após base limpa)

```
tests/
├── conftest.py                    ← fixtures globais
├── _archived/                     ← testes antigos (não executar)
│   ├── 2026-03-13_ARCHIVED_README.md
│   └── test_*.py                  ← versões antigas
├── smoke/
│   └── __init__.py                ← vazio, aguardando Fase 0
├── unit/
│   └── __init__.py                ← vazio, aguardando Fase 2
├── integration/
│   └── __init__.py                ← vazio, aguardando Fase 2
└── structural/
    └── __init__.py                ← vazio, aguardando Fase 2
```

---

## Como o Fluxo de Trabalho Funciona

```
AI executa tarefa no GitHub (push direto em main)
    ↓
Usuário: git pull
    ↓
Usuário: testa localmente
    ↓
Usuário: reporta resultado (OK ou erro específico)
    ↓
AI: ajusta se necessário OU avança para próxima tarefa
    ↓
(ciclo se repete)
```

---

## Contato Técnico do Projeto

- **GitHub:** `digimar07-cmyk`
- **Repo:** `dev-scratch-pad2`
- **Pasta:** `LASERFLIX_2/`
- **Branch principal:** `main`

---

## Vocabulário do Projeto

| Termo | Significado |
|-------|-------------|
| VOLKOV-01 | Código identificador da API pública do DatabaseManager |
| PERF-FIX-X | Prefixo de otimizações de performance no project_card |
| HOT-XX | Prefixo de hotfixes numerados |
| F-XX | Prefixo de features numeradas |
| FIX-CONTEXT-MENU | Fix específico do menu de contexto do card |
| Base Limpa | Operação de arquivamento e reorganização (2026-03-13) |
| Strangler Fig | Padrão de migração gradual sem reescrever do zero |
