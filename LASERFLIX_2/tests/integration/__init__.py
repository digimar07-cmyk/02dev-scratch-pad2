"""
tests/integration/__init__.py

Suite de testes de integracao do Laserflix.

Tipos de testes aqui:
  - Arquiteturais: garantem fronteiras de camada (core != ui, ai != ui)
  - Comportamentais: modulos reais colaborando sem mocks
  - Boundary: contratos de interface entre camadas

Convencao:
  test_*_boundary.py    = fronteira arquitetural + comportamento de contrato
  test_*_isolation.py   = isolamento de camada (subprocess ou AST)
  test_*_manager.py     = comportamento de alto nivel de um manager
"""
