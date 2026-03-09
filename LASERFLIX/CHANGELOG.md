# CHANGELOG - Laserflix

Todas as mudanças importantes serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [4.0.0.9] - 2026-03-09

### 🔧 FIX-REMOVE: Remoção via tela de seleção completamente corrigida

**Estado**: ✅ **CONCLUÍDA E TESTADA**

**Problemas corrigidos:**
- ✅ **FIX**: Cards removidos não desapareciam da tela após remoção (exigia navegar ao home)
- ✅ **FIX**: Contadores de categorias na sidebar não atualizavam após remoção via seleção
- ✅ **FIX**: Projetos removidos voltavam após reiniciar o app (persistência quebrada)

**Causa raiz identificada:**

| Arquivo | Bug | Correção |
|---|---|---|
| `selection_controller.py` | `db_manager.save()` não existe no `DatabaseManager` | `db_manager.save_database()` |
| `main_window.py` | `on_refresh_needed` não chamava `sidebar.refresh()` | Substituido por `_refresh_all()` |

**Detalhes técnicos:**
- `SelectionController.remove_selected()`: `self.db_manager.save()` → `self.db_manager.save_database()`
- `on_refresh_needed` em `main_window.py`: era `_invalidate_cache() + display_projects()` sem sidebar. Agora aponta diretamente para `_refresh_all()` que já faz cache + display + sidebar.
- `on_projects_removed`: extraido para método `_on_projects_removed()` dedicado (apenas atualiza status bar). O `_refresh_all()` chamado logo depois pelo controller cuida do resto.

**Arquivos modificados:**
1. `ui/controllers/selection_controller.py` - `save()` → `save_database()`
2. `ui/main_window.py` - `on_refresh_needed = _refresh_all`, novo `_on_projects_removed()`
3. `VERSION` - Atualizado para 4.0.0.9
4. `config/settings.py` - VERSION atualizado para 4.0.0.9
5. `CHANGELOG.md` - Este registro

**Commits:**
- `3647ba2` - FIX-REMOVE: db_manager.save() → save_database() em remove_selected
- `cb318fa` - FIX-REMOVE-REFRESH: on_refresh_needed inclui sidebar.refresh() + _refresh_all
- `07ae31f` - chore: bump version 4.0.0.2 → 4.0.0.9
- `b739870` - chore: bump VERSION em settings.py para 4.0.0.9

**Fluxo correto após fix:**
```
remove_selected()
  └─ del database[path]  (todos os selecionados)
  └─ db_manager.save_database()   ✔ persiste no JSON
  └─ collections_manager.save()   ✔ remove das coleções
  └─ on_mode_changed(False)        ✔ esconde SelectionBar
  └─ on_projects_removed(count)    ✔ atualiza status bar
  └─ on_refresh_needed()           ✔ _refresh_all()
       └─ _invalidate_cache()       ✔ força rebuild
       └─ display_projects()        ✔ tela sem os cards removidos
       └─ sidebar.refresh()         ✔ contadores atualizados
```

**Modelo usado**: Claude Sonnet 4.6

---

## [4.0.0.2] - 2026-03-08 17:32

### 🤖 MIGRAÇÃO DE MODELOS IA - QWEN3.5:4B

**Estado**: ✅ **CONCLUÍDA E TESTADA**

**Mudanças principais:**
- ✅ **REFACTOR**: Migrado de 7 modelos (24.3 GB) para 2 modelos (3.7 GB)
- ✅ **FEAT**: qwen3.5:4b multimodal (texto + visão em um único modelo)
- ✅ **FIX**: describe_image() agora usa /api/chat (multimodal)
- ✅ **PERF**: 71% menos modelos, 84.7% menos espaço em disco
- ✅ **PERF**: RAM máxima reduzida de ~14 GB para ~8 GB (-43%)
- ✅ **CONFIG**: settings.py atualizado com novos modelos
- ✅ **CONFIG**: Timeouts ajustados para qwen3.5:4b
- ✅ **PRESERVE**: Sistema de fallbacks intacto (100% funcional)

**Modelos removidos:**
```
❌ qwen2.5:3b-instruct-q4_K_M   (1.9 GB)
❌ qwen2.5:7b-instruct-q4_K_M   (4.7 GB)
❌ qwen2.5-coder:latest         (4.7 GB)
❌ llama3.1:latest              (4.9 GB)
❌ llama3.2-vision:latest       (7.8 GB)
❌ moondream:latest             (1.7 GB)
```

**Setup final:**
```
✅ qwen3.5:4b                   (3.4 GB) - texto + visão
✅ nomic-embed-text:latest      (274 MB) - embeddings
```

**Arquivos modificados:**
1. `config/settings.py` - Modelos atualizados + versão 4.0.0.2
2. `ai/ollama_client.py` - Método describe_image() usa /api/chat
3. `VERSION` - Atualizado para 4.0.0.2
4. `CHANGELOG.md` - Este registro

**Commits principais:**
- `6c952e6` - laserflix_v4.0.0.2_Stable (implementação inicial)
- `2491b58` - chore: Bump version para 4.0.0.2
- `7c59150` - chore: Atualiza versão e documentação em settings.py

**Sistema de fallbacks preservado:**
- ✅ Importação sem Ollama funciona (usa dicionários)
- ✅ Análise com Ollama offline usa fallback completo
- ✅ Categorias incompletas são completadas com fallback
- ✅ Zero quebras no workflow existente

**Modelo usado**: Claude Sonnet 4.5

**Instruções de uso:**
```bash
# 1. Pull do GitHub
git pull origin main

# 2. Verificar modelos (você já tem!)
ollama list
# Deve mostrar: qwen3.5:4b (3.4 GB) e nomic-embed-text:latest (274 MB)

# 3. Testar app
python main.py
```

---

## [3.4.3.4] - 2026-03-07 22:23:56

### 🎉 REFATORAÇÃO FASE-1A CONCLUÍDA

**Mudanças principais:**
- ✂️  Removido método `_update_chips_bar()` duplicado (~44 linhas)
- 🧹 Eliminadas todas as chamadas ao método obsoleto
- 📊 Redução: 868 → 646 linhas no `main_window.py` (-25.6%)
- ✅ App testado e funcional
- 💾 Backup automático criado (`.backup_20260307_222213`)

**Componentes existentes identificados:**
- `ui/components/chips_bar.py` - Já existia mas não estava integrado
- `ui/components/pagination_controls.py` - Próximo alvo FASE-1B
- `ui/components/selection_bar.py` - Próximo alvo FASE-1C

**Técnica aplicada:**
- Kent Beck "Tidy First" - Micro-refactorings incrementais
- Script 100% automático com validação de sintaxe
- Zero passos manuais

**Modelo usado**: Claude Sonnet 4.5

**Commits:**
- `4dbb8a6` - Mudança de versão + refatoração aplicada
- `39bb6d7` - Script de refatoração automática criado

**Próximos passos:**
- FASE-1B: Extrair/integrar `pagination_controls.py`
- FASE-1C: Extrair/integrar `selection_bar.py`
- FASE-1D: Simplificar `display_projects()` - Header

---

## [3.4.2.5] - 2026-03-07 09:13:00

### Sistema de versionamento automático implementado

**Mudanças:**
- Criado `version_manager.py` - Gerenciador de versões
- Criado arquivo `VERSION` para rastreamento único
- Criado `CHANGELOG.md` para histórico de mudanças
- Integrado com `apply_fase7_refactor.py`
- Auto-incremento de versão em cada modificação
- Atualização automática de `config/settings.py`
- Documentação de cada passo da refatoração

---

## [3.4.2.4] - 2026-03-07 08:00:00

### Versão stable com FASE 2 e FASE 3 aplicadas

**Mudanças:**
- FASE 2: DisplayController aplicado (filtros, ordenação, paginação)
- FASE 3: AnalysisController aplicado (análise IA, descrições)
- App funcional e testado
- 859 linhas de código

---

## [3.4.2.3] - 2026-03-06

### Estado anterior à refatoração Fase 7

**Mudanças:**
- Código original com 868 linhas
- Todas as funcionalidades inline no main_window.py

---
