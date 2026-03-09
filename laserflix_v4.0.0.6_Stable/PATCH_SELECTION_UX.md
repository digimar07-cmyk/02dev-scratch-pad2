# PATCH: Selection UX Refactor

## 📜 Mudanças MÍNIMAS Necessárias no `main_window.py`

### 1️⃣ ADICIONAR Import (linha ~54)

```python
from ui.managers.selection_bar_manager import SelectionBarManager
```

### 2️⃣ MODIFICAR `__init__` - Após `self._build_ui()` (linha ~155)

**ANTES:**
```python
self.root.configure(bg=BG_PRIMARY)
self._build_ui()

# === MANAGERS (criados DEPOIS de UI existir) ===
```

**DEPOIS:**
```python
self.root.configure(bg=BG_PRIMARY)
self._build_ui()

# === MANAGERS (criados DEPOIS de UI existir) ===
# UX-REFACTOR: SelectionBarManager (auto show/hide)
self.selection_bar_mgr = SelectionBarManager(
    parent_frame=self._content_frame,
    selection_ctrl=self.selection_ctrl,
    display_ctrl=self.display_ctrl,
    root=self.root
)
```

### 3️⃣ REMOVER callbacks antigos de selection_mode (linhas ~111-113)

**REMOVER ESTAS LINHAS:**
```python
self.selection_ctrl.on_mode_changed = self._on_selection_mode_changed
```

**MANTER:**
```python
# JÁ conectado via SelectionBarManager, não precisa mais aqui
self.selection_ctrl.on_selection_changed = self._on_selection_count_changed  # PODE REMOVER (opcional)
```

### 4️⃣ REMOVER métodos obsoletos (linhas ~259-270)

**REMOVER ESTES MÉTODOS:**
```python
# SELECTION CALLBACKS
def _on_selection_mode_changed(self, is_active: bool) -> None:
    if is_active:
        self._sel_bar.pack(fill="x", before=self.content_canvas.master)
        self.header.set_select_btn_active(True)
    else:
        self._sel_bar.pack_forget()
        self.header.set_select_btn_active(False)
    self._invalidate_cache()
    self.display_projects()

def _on_selection_count_changed(self, count: int) -> None:
    self._sel_count_lbl.config(text=f"{count} selecionado(s)")
    self._invalidate_cache()
    self.display_projects()
```

**NOTA:** O `_on_selection_count_changed` pode ser mantido se houver outras dependências, mas o manager já cuida disso.

### 5️⃣ REMOVER referência a `selection_mode` em `_should_rebuild()` (linha ~219)

**ANTES:**
```python
current_state = self.display_ctrl.get_display_state()
current_state["selection_mode"] = self.selection_ctrl.selection_mode
current_state["db_hash"] = (
```

**DEPOIS:**
```python
current_state = self.display_ctrl.get_display_state()
# UX-REFACTOR: selection_mode removido (não existe mais)
current_state["db_hash"] = (
```

### 6️⃣ REMOVER `selection_mode` de `_get_card_callbacks()` (linha ~354)

**ANTES:**
```python
return {
    "on_open_modal": self.open_project_modal,
    ...
    "selection_mode": self.selection_ctrl.selection_mode,
    "selected_paths": self.selection_ctrl.selected_paths,
```

**DEPOIS:**
```python
return {
    "on_open_modal": self.open_project_modal,
    ...
    # UX-REFACTOR: selection_mode removido (checkboxes sempre visíveis)
    "selected_paths": self.selection_ctrl.selected_paths,
```

### 7️⃣ REMOVER verificação de `selection_mode` em `open_project_modal()` (linha ~376)

**ANTES:**
```python
def open_project_modal(self, project_path: str) -> None:
    if self.selection_ctrl.selection_mode:
        self.selection_ctrl.toggle_project(project_path); return
    ProjectModal(
```

**DEPOIS:**
```python
def open_project_modal(self, project_path: str) -> None:
    # UX-REFACTOR: Sempre abre modal, checkbox é independente
    ProjectModal(
```

---

## ✅ Checklist de Verificação

- [ ] Import `SelectionBarManager` adicionado
- [ ] `self.selection_bar_mgr` instanciado após `_build_ui()`
- [ ] `on_mode_changed` callback removido
- [ ] Métodos `_on_selection_mode_changed` e `_on_selection_count_changed` removidos
- [ ] `selection_mode` removido de `_should_rebuild()`
- [ ] `selection_mode` removido de `_get_card_callbacks()`
- [ ] Verificação `if selection_mode:` removida de `open_project_modal()`

---

## 🚀 Teste Final

1. **Fazer pull:**
   ```bash
   git pull origin main
   ```

2. **Aplicar patch manualmente** (editar `main_window.py`)

3. **Rodar app:**
   ```bash
   python main.py
   ```

4. **Testar:**
   - [ ] Checkboxes visíveis no canto inferior direito de TODOS os cards
   - [ ] Clicar checkbox → Barra amarela aparece no topo
   - [ ] Contador mostra "1 selecionado(s)"
   - [ ] Clicar em outro checkbox → Contador atualiza "2 selecionado(s)"
   - [ ] Botão "Remover selecionados" habilitado
   - [ ] Desmarcar todos → Barra desaparece automaticamente
   - [ ] Clicar na capa do card → Abre modal (não seleciona)
   - [ ] Menu de contexto (botão direito) → Funciona normalmente

---

## 📊 Estatísticas

**Linhas removidas do `main_window.py`:** ~30 linhas  
**Linhas adicionadas:** ~8 linhas  
**Redução líquida:** -22 linhas  

**Novos arquivos criados:**
- `ui/managers/selection_bar_manager.py` (+100 linhas)

**Arquivos modificados:**
- `ui/controllers/selection_controller.py` (-40 linhas)
- `ui/project_card.py` (+5 linhas, -15 linhas)
- `ui/builders/ui_builder.py` (-5 linhas)

**Benefícios:**
- ✅ Lógica de seleção totalmente desacoplada do `main_window.py`
- ✅ UX mais intuitiva (checkboxes sempre visíveis)
- ✅ Auto show/hide da barra de seleção
- ✅ Código mais modular e testável
- ✅ Preparação para FASE-3 (desmembramento total)
