# Metodologia Akita — Guia Extraído do Blog

> Documento base que governa todo o desenvolvimento Laserflix v4.0.
> Fonte: blog.akitaonrails.com — série sobre Vibe Coding e XP

---

## Os 12 Princípios Aplicados ao Laserflix

### 1. Extreme Programming (XP) como base

> *"Programar Vibe Coding da forma correta só tem um jeito: Extreme Programming!"*

XP não é sobre velocidade — é sobre **ritmo sustentável com qualidade garantida**.
Cada prática do XP existe para eliminar uma categoria específica de risco.

**Aplicação no Laserflix:**
- Nenhuma feature nova sem contrato de teste
- Refatoração contínua, não acumulada
- Commits pequenos e descritivos (nunca `git add .`)

---

### 2. Test-Driven Development (TDD) — Red/Green/Refactor

> *"Todo código sem teste é código com prazo de validade."*

O ciclo obrigatório:
```
RED   → Escrever o teste que falha (define o contrato)
GREEN → Escrever o mínimo de código para passar
REFACTOR → Limpar sem quebrar o teste
```

**Regras absolutas:**
- Bug encontrado = teste de regressão ANTES do fix
- Feature nova = teste ANTES do código
- Refatoração = zero novos testes (comportamento não muda)

---

### 3. CI Sempre Verde

> *"Se o CI está vermelho, NADA mais entra no repositório."*

O estado natural do `main` é: **todos os testes passando**.
Se quebrar, consertar é prioridade zero — acima de qualquer feature.

**Aplicação no Laserflix:**
- `pytest` deve passar antes de qualquer commit
- Script `QA/run_all.bat` é o portão de entrada
- Falha no structural test = arquivo precisa ser quebrado antes do commit

---

### 4. Small Commits — Commits Atômicos

> *"Commits pequenos são o diário de decisões do projeto."*

Cada commit deve:
- Fazer UMA coisa
- Ter mensagem descritiva no formato `tipo(escopo): descrição`
- Deixar o projeto em estado funcional

**Tipos de commit usados:**
```
feat     → nova funcionalidade
fix      → correção de bug
refactor → mudança de código sem mudar comportamento
test     → adiciona/modifica testes
docs     → documentação
chore    → tarefas de manutenção (configs, deps)
```

---

### 5. Tidy First (Kent Beck)

> *"Arrume a casa ANTES de adicionar novos móveis."*

Antes de qualquer feature nova, o código existente deve estar organizado.
Refatoração e funcionalidade são commits SEPARADOS — nunca misturar.

**Aplicação prática:**
- Fase 4 (refatoração) ANTES da Fase 6 (melhorias)
- `recursive_import_integration.py` deve ser quebrado ANTES de novas features

---

### 6. Cobertura de Testes com Propósito

> *"Akita no FrankMD chegou a 70% de cobertura; no Chronicles, 100%."*

**Metas por tipo de módulo:**
```
core/     → 90%+ (regras de negócio, risco alto)
ai/       → 75%+ (comportamento não-determinístico, risco alto)
utils/    → 85%+ (utilitários, fácil de testar)
ui/       → 50%+ (difícil mockar Tkinter, pragmático)
config/   → 60%+ (estrutura de dados)
```

**Tipos de teste e seu propósito:**
```
unit/        → testa UMA função/classe isolada, sem I/O real
integration/ → testa DOIS+ módulos colaborando, com I/O controlado
smoke/       → testa que o sistema SOBE sem erro (CI gate mínimo)
structural/  → testa que REGRAS ARQUITETURAIS não foram violadas
```

---

### 7. Separação de Camadas — core/ nunca importa ui/

> *"Dependência invertida: regras de negócio não conhecem a UI."*

**Hierarquia de dependências (do mais baixo para o mais alto):**
```
config/   ← não importa nada do projeto
utils/    ← importa apenas config/
core/     ← importa config/ e utils/
ai/       ← importa config/, utils/ e core/
ui/       ← importa tudo (é o topo da pilha)
```

**Teste estrutural obrigatório:** `core/` não pode conter `import tkinter`.

---

### 8. Strangler Fig — Nunca Reescrever do Zero

> *"Substitua sistemas legados gradualmente, nunca jogue fora e reescreva."*

Aplicação na migração JSON → SQLite:
- `DatabaseManagerSQLite` implementa API idêntica ao `DatabaseManager`
- Feature flag controla qual backend está ativo
- Migração com script validado, não manual
- Rollback possível em qualquer ponto

---

### 9. Programação Defensiva com Logs Corretos

**Regra de logging:**
```python
# ERRADO — f-string sempre avaliada, mesmo com log desativado:
self.logger.debug(f"Carregados {count} projetos")

# CORRETO — lazy evaluation, só avalia se o nível estiver ativo:
self.logger.debug("Carregados %d projetos", count)
```

**Regra de exception handling:**
- Nunca `except Exception: pass` sem log
- Capturar exceções específicas, não genéricas
- Cada `except` deve ter uma ação defensiva explícita

---

### 10. API Pública com Contrato Documentado

> *"Código é comunicação. O contrato da API é a primeira linha de documentação."*

Cada classe pública deve ter:
- Docstring listando todos os métodos públicos
- Type hints em todos os parâmetros e retornos
- Nenhum método público sem documentação de comportamento

Exemplo modelo (DatabaseManager — o melhor arquivo do projeto):
```python
"""
API pública (VOLKOV-01):
  get_project(path)      → dict | None
  set_project(path,data) → None
  remove_project(path)   → bool
"""
```

---

### 11. Limite de Tamanho de Arquivo — Guardião Automático

> *"Arquivo grande = responsabilidade grande = risco grande."*

Limites definidos (aplicados pelo teste structural/test_file_sizes.py):
```
core/    → 15.000 bytes máximo
ui/      → 20.000 bytes máximo  
utils/   → 10.000 bytes máximo
ai/      → 15.000 bytes máximo
config/  →  8.000 bytes máximo
```

Se o teste falhar: **o arquivo deve ser quebrado antes do commit**.

---

### 12. Documentação Viva — O Código É a Documentação

> *"Comentários que explicam O QUÊ o código faz são sinais de código ruim."*

**Comentários bons** explicam o PORQUÊ da decisão:
```python
# FIX-CONTEXT-MENU: Deve ser chamado DEPOIS de criar todos os widgets.
# Problema original: chamado cedo demais, filhos não recebiam o bind.
# Solução: recursivo no FINAL do build_card().
_bind_context_menu_recursive(card, context_menu_handler)
```

**Comentários ruins** descrevem o óbvio:
```python
# Incrementa o contador (RUIM — óbvio pelo código)
count += 1
```

---

## Aplicação ao Ciclo de Desenvolvimento

```
Para CADA tarefa do plano:

1. Ler o requisito
2. Escrever o teste (RED)
3. Rodar: pytest → confirmar que FALHA pelo motivo certo
4. Implementar o mínimo para passar (GREEN)
5. Rodar: pytest → confirmar que PASSA
6. Refatorar se necessário (REFACTOR)
7. Rodar: pytest → confirmar que ainda PASSA
8. Commit atômico com mensagem descritiva
9. Reportar ao usuário para aprovação antes da próxima tarefa
```
