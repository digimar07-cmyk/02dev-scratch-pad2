"""
Configurações centralizadas do Laserflix v4.0.1.3
"""
from __future__ import annotations
import os

# Diretório raiz do projeto (pasta onde este arquivo está, um nível acima de config/)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================================
# VERSÃO
# ============================================================================
VERSION = "4.0.1.3"

# ============================================================================
# ARQUIVOS E DIRETÓRIOS — paths absolutos, independentes do cwd
# ============================================================================
CONFIG_FILE   = os.path.join(_ROOT, "laserflix_config.json")
DB_FILE       = os.path.join(_ROOT, "laserflix_database.json")
BACKUP_FOLDER = os.path.join(_ROOT, "laserflix_backups")
LOG_FILE      = os.path.join(_ROOT, "laserflix.log")

# ============================================================================
# CONFIGURAÇÃO OLLAMA
# ============================================================================
OLLAMA_BASE_URL      = "http://localhost:11434"
OLLAMA_RETRIES       = 3
OLLAMA_HEALTH_TIMEOUT    = 4
OLLAMA_HEALTH_CACHE_TTL  = 5.0  # segundos

# ============================================================================
# MODELOS - MIGRAÇÃO PARA QWEN3.5:4B (v4.0.0.2)
# ============================================================================
# ANTES (v3.x): 7 modelos, 24.3 GB
# DEPOIS (v4.0.0.2): 2 modelos, 3.7 GB (economia de 84.7%)
OLLAMA_MODELS = {
    "text_quality": "qwen3.5:4b",             # análise individual, descrições
    "text_fast":    "qwen3.5:4b",             # lotes grandes (>50 projetos)
    "vision":       "qwen3.5:4b",             # análise de imagem de capa
    "embed":        "nomic-embed-text:latest", # embeddings (reservado)
}

FAST_MODEL_THRESHOLD = 50

# ============================================================================
# TIMEOUTS - AJUSTADOS PARA QWEN3.5:4B
# ============================================================================
TIMEOUTS = {
    "text_quality": (5, 120),
    "text_fast":    (5, 75),
    "vision":       (5, 60),
    "embed":        (5, 15),
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
    "max_white_pct":  50,
}

# ============================================================================
# BACKUP AUTOMÁTICO
# ============================================================================
AUTO_BACKUP_INTERVAL_MS = 1800000  # 30 minutos
MAX_AUTO_BACKUPS = 10

# ============================================================================
# LOGGING
# ============================================================================
LOG_MAX_BYTES    = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3
