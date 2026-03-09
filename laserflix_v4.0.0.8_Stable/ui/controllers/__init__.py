"""
ui/controllers/ - Camada de Controllers (MVC)

Separa lógica de coordenação da UI.
Controllers orquestram operações entre UI e Core.

⚠️ REGRA ABSOLUTA: Nenhum controller pode ter > 300 linhas!

Controllers ativos (09/03/2026):
  - optimized_display_controller.py  ← display e filtros
  - selection_controller.py          ← modo seleção e remoção
  - analysis_controller.py           ← análise IA
  - collection_controller.py         ← coleções

📦 REMOVIDOS:
  - display_controller.py            ← LEGADO (substituído por optimized)
  - project_management_controller.py ← MORTO (sem imports)
  - modal_manager.py                 ← MOVIDO para ui/managers/
"""
