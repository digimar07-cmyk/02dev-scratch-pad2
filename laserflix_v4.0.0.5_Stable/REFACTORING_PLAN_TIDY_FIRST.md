# 🎯 PLANO DE REFATORAÇÃO "TIDY FIRST" - LASERFLIX v3.4.3.4

**Criado em**: 07/03/2026 21:25 BRT  
**Última atualização**: 08/03/2026 19:07 BRT (Pós-auditoria)  
**Modelo usado**: Claude Sonnet 4.5  
**Baseado em**: Kent Beck "Tidy First", Simple Design, XP Refactoring

---

## 🚨 AVISO IMPORTANTE

⚠️ **Este documento contém o workflow e filosofia de refatoração.**

📊 **Para status atual detalhado, consulte**: [`REFACTORING_STATUS.md`](./REFACTORING_STATUS.md)

O `REFACTORING_STATUS.md` é a **fonte única da verdade** (single source of truth) atualizada após cada fase.

---

## 📊 ESTADO ATUAL (08/03/2026)

```
Arquivo: ui/main_window.py
Linhas originais: ~868 linhas (07/03/2026)
Linhas atuais: ~646 linhas (08/03/2026)
Limite: 200 linhas (FILE_SIZE_LIMIT_RULE.md)
Status: ⚠️  AINDA EM VIOLAÇÃO
Excesso: ~446 linhas (223% acima do limite)
Progresso: 25.6% concluído

Fases concluídas: 8
Fases pendentes: 5
Fases canceladas: 1
```

**👉 Ver detalhes em**: [`REFACTORING_STATUS.md`](./REFACTORING_STATUS.md)

---

## 🔥 WORKFLOW ABSOLUTO DE REFATORAÇÃO

**REGRA #0 (08/03/2026)**: **WORKFLOW OBRIGATÓRIO PARA TODA REFATORAÇÃO**

### Sequência Inviolável:

```
1️⃣ ANALISAR A TAREFA
   - Ler descrição completa
   - Entender objetivo da refatoração
   - Identificar arquivo(s) alvo
   - Verificar tamanho atual vs limite

2️⃣ VERIFICAR CÓDIGO DUPLICADO
   - Procurar por métodos/funções similares
   - Identificar padrões repetidos
   - Buscar lógica idêntica em múltiplos locais
   - Documentar todas as duplicações encontradas

3️⃣ SE DUPLICAÇÃO EXISTE
   ❌ NÃO PROSSEGUIR COM REFATORAÇÃO
   ✅ DAR INSTRUÇÕES PARA RESOLVER:
      - Listar todas as duplicações encontradas
      - Especificar qual código manter (fonte canônica)
      - Indicar quais trechos deletar
      - Sugerir método unificado (se aplicável)
      - Esperar aprovação do usuário
   
4️⃣ SE NÃO EXISTE DUPLICAÇÃO
   ✅ PROSSEGUIR COM TAREFA:
   
   4.1. Criar nova função/classe/componente
        - Seguir padrões existentes
        - Nomear claramente (expressar intenção)
        - Documentar parâmetros e retorno
   
   4.2. Testar função isoladamente (se possível)
        - Validar sintaxe Python
        - Verificar imports necessários
   
   4.3. Apagar código do arquivo original
        - Marcar linhas removidas no commit
        - Criar backup antes (script automático)
   
   4.4. Fazer conexão para funcionar
        - Adicionar import da nova função
        - Substituir chamadas antigas
        - Passar parâmetros corretos
        - Manter comportamento idêntico
   
   4.5. Validar integração
        - Verificar sintaxe completa
        - Conferir todos os imports
        - Simular fluxo de execução

5️⃣ FAZER COMMIT
   - Mensagem no formato: refactor(FASE-XX): descrição (-N lines)
   - Incluir arquivo modificado
   - Push para branch main (ou branch específica)

6️⃣ AVISAR USUÁRIO
   ✅ "COMMIT FEITO - PRONTO PARA TESTAR"
   📝 Informar:
      - Arquivo modificado
      - Linhas removidas
      - O que foi extraído
      - Como testar
      - Branch/commit
   
7️⃣ AGUARDAR OK DO USUÁRIO
   ⏸️ **PARAR AQUI**
   - Não continuar próxima fase
   - Não fazer novos commits
   - Esperar confirmação: "OK" ou "testado e funciona"
   - Se usuário reportar bug → reverter para backup

8️⃣ SE OK RECEBIDO
   ✅ Marcar fase como concluída
   ✅ Atualizar REFACTORING_STATUS.md
   ✅ Prosseguir para próxima fase
```

---

### ⚠️ CONSEQUÊNCIAS DE VIOLAÇÃO DO WORKFLOW

**SE NÃO SEGUIR WORKFLOW**:
- ❌ Refatoração rejeitada
- ❌ Commit não será feito
- ❌ Reiniciar processo desde etapa 1️⃣

**SE PULAR ETAPA 3️⃣ (verificação de duplicação)**:
- 🐛 Bugs silenciosos (código morto permanece)
- 📈 Arquivo não diminui o esperado
- 🔄 Retrabalho futuro

**SE NÃO AGUARDAR OK (etapa 7️⃣)**:
- ⚠️ Risco de sobrescrever com próxima fase
- 🔧 Dificulta identificar qual fase quebrou
- 💥 Pode acumular bugs sem detecção

---

## ✅ FILOSOFIA KENT BECK APLICADA

### 4 Regras de Simple Design:
1. ✅ **Passa todos os testes** (manual OK por agora)
2. ✅ **Sem duplicação** (unificar código repetido) ← **REFORÇADO PELO WORKFLOW**
3. ✅ **Expressa intenção** (nomes claros)
4. ✅ **Mínimo de elementos** (extrair só o necessário)

### Princípios "Tidy First":
- **Tidy First** = Arrumar ANTES de adicionar features
- **Micro-refactorings** = Mudanças de 5-15 minutos cada
- **Não cruzar os raios** = Nunca misturar refatoração + comportamento
- **Commits atômicos** = 1 mudança → 1 commit → 1 teste
- **Workflow rigoroso** = Seguir sequência inviolável (WORKFLOW ABSOLUTO)
- **Fonte única da verdade** = REFACTORING_STATUS.md sempre atualizado

---

## 📅 ROADMAP RESUMIDO

**👉 Para detalhes completos, ver**: [`REFACTORING_STATUS.md`](./REFACTORING_STATUS.md)

| Fase | Status | Redução | Linhas Após |
|------|--------|---------|-------------|
| **Original** | - | - | 868 |
| **FASE-1A** | ✅ Concluída | -222 | 646 |
| **FASE-1B** | ❌ Cancelada | - | 646 |
| **FASE-1C** | ⚠️ Próxima | -40 | 606 |
| **FASE-2** | ⚪ Pendente | -80 | 526 |
| **FASE-3** | ⚪ Pendente | -45 | 481 |
| **FASE-4** | ⚪ Pendente | -100 | 381 |
| **FASE-5** | ⚪ Pendente | -50 | **331** |

**Meta final**: ~331 linhas (62% de redução total)

---

## 👉 PRÓXIMA AÇÃO

### FASE-1C: Integrar SelectionBar

**Status**: ⏸️ **AGUARDANDO APROVAÇÃO**

**Duplicação confirmada**:
- ✅ Componente `ui/components/selection_bar.py` existe (176 linhas)
- ❌ UIBuilder tem código duplicado em `_build_selection_bar()`
- ❌ main_window usa `_sel_bar` e `_sel_count_lbl` diretamente

**Solução proposta**:
1. Manter `selection_bar.py` como fonte canônica
2. Deletar `UIBuilder._build_selection_bar()` (~45 linhas)
3. Importar e instanciar `SelectionBar` no main_window
4. Conectar callbacks ao `SelectionController`
5. Substituir referências diretas por métodos do componente

**Redução esperada**: -40 linhas (646 → 606)

**👉 Ver instruções detalhadas em**: [`REFACTORING_STATUS.md`](./REFACTORING_STATUS.md#fase-1c-integrar-selectionbar-pendente)

---

## 🔒 PROTOCOLO DE EXECUÇÃO

### Para CADA micro-refactoring:

```bash
# 1. Fazer pull para sincronizar
git pull origin main

# 2. Executar script automático (quando disponível)
python REFACTOR_AUTO_FASE_XX.py

# 3. Testar MANUALMENTE
python main.py
# Testar funcionalidade afetada

# 4. Se funciona:
git add .
git commit -m "refactor(FASE-XX): descrição clara (-X lines)"
git push origin main

# 5. Atualizar REFACTORING_STATUS.md
# [Automatizado via commit do assistente]

# 6. Se quebrou:
# Restaurar backup criado pelo script
cp ui/main_window.py.backup_YYYYMMDD_HHMMSS ui/main_window.py
```

---

## ⚠️ REGRAS ABSOLUTAS

### Durante refatoração:

1. ❌ **NÃO adicionar features** - Apenas mover código
2. ❌ **NÃO mudar comportamento** - Apenas estrutura
3. ❌ **NÃO fazer commits grandes** - Máximo 100 linhas por commit
4. ✅ **SEMPRE testar após cada commit** - Manual OK
5. ✅ **SEMPRE usar scripts automáticos** - Reduz erros humanos
6. ✅ **SEMPRE commitar com mensagem clara** - Facilita git log
7. ✅ **SEMPRE seguir WORKFLOW ABSOLUTO** - Etapas 1-8 invioláveis
8. ✅ **SEMPRE verificar duplicação ANTES** - Etapa 2 obrigatória
9. ✅ **SEMPRE aguardar OK do usuário** - Etapa 7 obrigatória
10. ✅ **SEMPRE atualizar REFACTORING_STATUS.md** - Após cada fase

### Após cada fase:

1. ✅ Atualizar [`REFACTORING_STATUS.md`](./REFACTORING_STATUS.md) com status
2. ✅ Registrar linhas reais removidas
3. ✅ Documentar problemas encontrados
4. ✅ Commit de checkpoint
5. ✅ **Aguardar confirmação do usuário antes de próxima fase**

---

## 📝 LOG DE PROGRESSO

### 08/03/2026 19:07 BRT - Auditoria Completa + Sincronização
- ✅ Auditoria completa do código vs documentação realizada
- ✅ REFACTORING_STATUS.md criado como fonte única da verdade
- ✅ Este plano atualizado com cross-references
- ✅ FASE-1B marcada como CANCELADA (duplicada com FASE-1.1)
- ✅ FASE-1C confirmada como próxima tarefa
- ✅ 8 fases concluídas identificadas
- ✅ 5 fases pendentes mapeadas
- ✅ 2 arquivos obsoletos identificados
- ✅ Roadmap de redução recalculado

### 08/03/2026 18:57 BRT - WORKFLOW ABSOLUTO Incorporado
- ✅ Regra #0 adicionada ao documento
- ✅ Sequência de 8 etapas definida
- ✅ Exemplos práticos incluídos
- ✅ Consequências de violação documentadas
- ✅ Todas as fases atualizadas para seguir workflow
- ✅ Pronto para aplicação imediata

### 07/03/2026 22:40 BRT - Atualização de Documentação
- ✅ Plano atualizado com resultado FASE-1A
- ✅ CHANGELOG.md atualizado com v3.4.3.4
- ✅ VERSION atualizado para 3.4.3.4
- ✅ Documentação sincronizada com GitHub

### 07/03/2026 22:23 BRT - FASE-1A Concluída
- ✅ Script `REFACTOR_AUTO_FASE_1A.py` executado com sucesso
- ✅ Método `_update_chips_bar()` removido (44 linhas)
- ✅ 5 chamadas ao método removidas
- ✅ 222 linhas totais eliminadas (868 → 646)
- ✅ App testado e funcional
- ✅ Backup criado: `main_window.py.backup_20260307_222213`
- ✅ Commit `4dbb8a6` aplicado

### 07/03/2026 21:25 BRT - Plano Criado
- ✅ Plano criado
- ✅ Documentação antiga arquivada
- ✅ Script FASE-1A criado

---

## 📊 DOCUMENTOS RELACIONADOS

### Fonte Única da Verdade
- **[REFACTORING_STATUS.md](./REFACTORING_STATUS.md)** - Status detalhado atualizado após cada fase

### Documentação de Apoio
- **[FILE_SIZE_LIMIT_RULE.md](./FILE_SIZE_LIMIT_RULE.md)** - Regra de limite de 200 linhas
- **[CHANGELOG.md](./CHANGELOG.md)** - Histórico de versões
- **[VERSION](./VERSION)** - Versão atual do sistema

---

**Modelo usado**: Claude Sonnet 4.5  
**Filosofia**: Kent Beck "Tidy First" + Simple Design + **WORKFLOW ABSOLUTO**  
**Garantia**: Micro-refactorings seguros e incrementais com aprovação em cada etapa  
**Status atual**: 👉 **VER REFACTORING_STATUS.md** ← **FONTE ÚNICA DA VERDADE**
