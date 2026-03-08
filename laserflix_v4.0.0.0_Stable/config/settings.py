"""
Configurações centralizadas do Laserflix v4.0.1.0
"""
import os

# ============================================================================
# VERSÃO
# ============================================================================
VERSION = "4.0.1.0"

# ============================================================================
# ARQUIVOS E DIRETÓRIOS
# ============================================================================
CONFIG_FILE = "laserflix_config.json"
DB_FILE = "laserflix_database.json"
BACKUP_FOLDER = "laserflix_backups"
LOG_FILE = "laserflix.log"

# ============================================================================
# CONFIGURAÇÃO OLLAMA
# ============================================================================
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_RETRIES = 3
OLLAMA_HEALTH_TIMEOUT = 4
OLLAMA_HEALTH_CACHE_TTL = 5.0  # segundos

# ============================================================================
# MODELOS - MIGRAÇÃO PARA QWEN3.5:4B (v4.0.1)
# ============================================================================
# ANTES (v3.x): 7 modelos, 24.3 GB
# DEPOIS (v4.0.1): 2 modelos, 3.7 GB (economia de 84.7%)
#
# qwen3.5:4b é multimodal (texto + visão), substituindo:
#   - qwen2.5:7b (texto qualidade)
#   - qwen2.5:3b (texto rápido)
#   - qwen2.5-coder (análise de código)
#   - llama3.1 (chat)
#   - llama3.2-vision (visão)
#   - moondream (visão antiga)
# ============================================================================
OLLAMA_MODELS = {
    "text_quality": "qwen3.5:4b",              # análise individual, descrições
    "text_fast":    "qwen3.5:4b",              # lotes grandes (mesmo modelo, rápido)
    "vision":       "qwen3.5:4b",              # análise de imagem (multimodal)
    "embed":        "nomic-embed-text:latest",  # embeddings (sem mudança)
}

# Limiar: acima deste número de projetos, usa modelo rápido no lote
# NOTA: Com qwen3.5:4b, text_fast e text_quality são o mesmo modelo,
#       mas mantemos a lógica para futura granularidade
FAST_MODEL_THRESHOLD = 50

# ============================================================================
# TIMEOUTS - AJUSTADOS PARA QWEN3.5:4B
# ============================================================================
# Timeouts por tipo de modelo (connect_timeout, read_timeout)
TIMEOUTS = {
    "text_quality": (5, 120),  # análise individual (mesmo timeout)
    "text_fast":    (5, 90),   # lotes (mesmo modelo, mais rápido)
    "vision":       (5, 90),   # visão multimodal (ajustado de 60s)
    "embed":        (5, 15),   # embeddings (sem mudança)
}

# ============================================================================
# CACHE DE THUMBNAILS
# ============================================================================
THUMBNAIL_CACHE_LIMIT = 300
THUMBNAIL_SIZE = (220, 200)

# ============================================================================
# QUALIDADE DE IMAGEM (FILTRO PARA VISÃO)
# ============================================================================
IMAGE_QUALITY_THRESHOLDS = {
    "max_brightness": 210,
    "min_saturation": 25,
    "max_white_pct": 50,
}

# ============================================================================
# BACKUP AUTOMÁTICO
# ============================================================================
AUTO_BACKUP_INTERVAL_MS = 1800000  # 30 minutos
MAX_AUTO_BACKUPS = 10

# ============================================================================
# LOGGING
# ============================================================================
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5MB
LOG_BACKUP_COUNT = 3
