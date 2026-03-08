# 🤖 Modelos de IA - Laserflix v4.0

**Atualizado**: 08/03/2026  
**Hardware**: Intel i5-4440 (4 cores, 3.1GHz) | 24GB RAM DDR3 | GTX 1050 Ti

---

## 📦 Modelos Instalados

### Modelo Principal: Qwen 3.5 (4B)

```bash
qwen3.5:4b
```

**Tamanho**: 3.4 GB  
**RAM em uso**: ~6-8 GB  
**Contexto**: 256K tokens  
**Capacidades**: Texto + Visão (multimodal)

#### Funções no Laserflix

| Função | Uso | Antes (múltiplos modelos) |
|--------|-----|---------------------------|
| **Análise de código** | Geração de categorias/tags | qwen2.5-coder:7b (4.7 GB) |
| **Geração de texto** | Descrições de produtos | qwen2.5:7b + qwen2.5:3b (6.6 GB) |
| **Análise de imagem** | Descrição visual de capas | llama3.2-vision:7b (7.8 GB) |
| **Chat geral** | Interações rápidas | llama3.1:latest (4.9 GB) |

**Total economizado**: 20.6 GB (de 24.3 GB → 3.7 GB)

#### Benchmarks Internos

```
Análise de projeto individual : ~3-5s
Lote de 10 projetos          : ~30-40s
Geração de descrição         : ~4-6s
Análise de imagem (512x512)  : ~5-8s
```

---

### Modelo de Embeddings: Nomic Embed Text

```bash
nomic-embed-text:latest
```

**Tamanho**: 274 MB  
**Dimensões**: 768d  
**Uso**: Busca semântica bilíngue (EN/PT-BR)

#### Funções no Laserflix

- Embeddings de nomes de projetos
- Busca por similaridade semântica
- Sugestões de projetos relacionados (futuro)

---

## 🔄 Histórico de Modelos

### Versão 3.x (anterior - REMOVIDO)

```bash
# Modelos antigos (total: 24.3 GB)
qwen2.5:3b-instruct-q4_K_M   # 1.9 GB - texto rápido
qwen2.5:7b-instruct-q4_K_M   # 4.7 GB - texto qualidade
qwen2.5-coder:latest         # 4.7 GB - análise de código
llama3.1:latest              # 4.9 GB - chat geral
llama3.2-vision:latest       # 7.8 GB - análise de imagem
moondream:latest             # 1.7 GB - visão (desatualizado)
nomic-embed-text:v1.5        # 274 MB - duplicata
```

**Problemas**:
- ❌ Redundância funcional (7 modelos, 5 funções)
- ❌ 24.3 GB de espaço em disco
- ❌ Complexidade de configuração
- ❌ Alto consumo de RAM ao trocar modelos

### Versão 4.0 (atual - OTIMIZADO)

```bash
# Setup minimalista (total: 3.7 GB)
qwen3.5:4b                   # 3.4 GB - tudo-em-um
nomic-embed-text:latest      # 274 MB - embeddings
```

**Vantagens**:
- ✅ Um modelo = todas as funções
- ✅ 84.7% menos espaço em disco
- ✅ Simplicidade de manutenção
- ✅ Performance equivalente ou superior
- ✅ Multimodal nativo (texto + visão)

---

## ⚙️ Configuração no Código

### config/settings.py

```python
OLLAMA_MODELS = {
    "text_quality": "qwen3.5:4b",         # análise individual
    "text_fast":    "qwen3.5:4b",         # lotes (mesmo modelo)
    "vision":       "qwen3.5:4b",         # análise de imagem
    "embed":        "nomic-embed-text:latest",
}
```

### Timeouts Ajustados

```python
TIMEOUTS = {
    "text_quality": (5, 120),  # connect, read (segundos)
    "text_fast":    (5, 90),   # mesmo modelo, timeout menor
    "vision":       (5, 90),   # visão multimodal
    "embed":        (5, 15),   # embeddings rápidos
}
```

---

## 🚀 Como Usar

### Análise de Projeto com IA

```python
from ai.text_generator import TextGenerator

# Analisa projeto e retorna categorias/tags
categories, tags = generator.analyze_project(project_path)
```

**Modelo usado**: qwen3.5:4b (role: text_quality ou text_fast)

### Análise de Imagem

```python
from ai.image_analyzer import ImageAnalyzer

# Descreve imagem (filtro de qualidade aplicado automaticamente)
description = analyzer.analyze_cover(image_path)
```

**Modelo usado**: qwen3.5:4b (role: vision)

### Geração de Descrição

```python
# Gera descrição comercial personalizada
description = generator.generate_description(project_path, project_data)
```

**Modelo usado**: qwen3.5:4b (role: text_quality, temp: 0.78)

---

## 🔍 Detalhes Técnicos

### Qwen 3.5 (4B) - Especificações

**Arquitetura**: Transformer multimodal  
**Parâmetros**: 4 bilhões  
**Quantização**: Q4_K_M (4-bit)  
**Treinamento**: Março 2026  
**Contexto máximo**: 256K tokens

**Capacidades**:
- ✅ Geração de texto em português brasileiro
- ✅ Análise de código Python/JavaScript
- ✅ Visão computacional (OCR, descrição de imagens)
- ✅ Raciocínio estruturado
- ✅ Few-shot learning

**Limitações**:
- ⚠️ Não é especializado em tradução
- ⚠️ Pode alucinar com prompts muito abstratos
- ⚠️ Requer prompts bem estruturados para melhores resultados

### Estratégias de Prompt

#### Para Análise (categorias/tags)

```python
prompt = """Analise este produto de corte laser e responda EXATAMENTE no formato solicitado.

📁 NOME: {name}
📊 ARQUIVOS: {structure}
🗂️ TIPOS: {file_types}
🖼️ DESCRIÇÃO VISUAL: {vision_desc}

### TAREFA 1 — CATEGORIAS (MÍNIMO 10)
[instruções detalhadas...]

### FORMATO DE RESPOSTA:
Categorias: [cat1], [cat2], ...
Tags: [tag1], [tag2], ...
"""
```

**Temperature**: 0.65 (criatividade controlada)  
**Tokens**: 300

#### Para Descrição (texto comercial)

```python
prompt = """Você é especialista em peças físicas de corte a laser.

NOME DA PEÇA: {clean_name}
DETALHE VISUAL: {vision_context}

### RACIOCINE antes de escrever:
1. O que exatamente é esta peça física?
2. Para que serve na prática?
3. Que emoção ela representa?

### FORMATO DE SAÍDA:
{clean_name}

🎨 Por Que Este Produto é Especial:
[2-3 frases afetivas]

💖 Perfeito Para:
[2-3 frases práticas]
"""
```

**Temperature**: 0.78 (mais criatividade)  
**Tokens**: 250

---

## 📊 Comparação de Performance

| Métrica | v3.x (7 modelos) | v4.0 (2 modelos) | Melhoria |
|---------|------------------|------------------|----------|
| **Espaço em disco** | 24.3 GB | 3.7 GB | **84.7%** ↓ |
| **RAM máxima** | ~14 GB | ~8 GB | **43%** ↓ |
| **Tempo de troca** | ~3-5s | 0s (mesmo modelo) | **100%** ↓ |
| **Complexidade config** | 7 modelos | 2 modelos | **71%** ↓ |
| **Funções cobertas** | 5 | 5 | **100%** ✓ |
| **Qualidade output** | Alta | Equivalente/Superior | **✓** |

---

## 🛠️ Troubleshooting

### Problema: qwen3.5:4b não encontrado

```bash
# Instalar modelo
ollama pull qwen3.5:4b

# Verificar instalação
ollama list
```

### Problema: Análise de imagem não funciona

**Verificações**:
1. Imagem passa no filtro de qualidade? (veja logs)
2. qwen3.5:4b está rodando? (`ollama ps`)
3. Timeout suficiente? (padrão: 90s)

**Critérios de qualidade** (image_analyzer.py):
- Brilho médio < 210
- Saturação média > 25
- Fundo branco < 50%

### Problema: Ollama retorna respostas vazias

**Causas comuns**:
1. Modelo não baixado completamente
2. RAM insuficiente (qwen3.5:4b precisa ~8 GB)
3. Timeout muito curto
4. Ollama travado (reinicie: `ollama serve`)

**Solução**: O Laserflix tem fallbacks automáticos! Mesmo sem IA, funciona.

---

## 🔮 Roadmap

### Futuras Melhorias

**v4.1** (Q2 2026):
- [ ] Fine-tuning do qwen3.5:4b com dataset de projetos laser
- [ ] Embeddings visuais (quando disponível no Ollama)
- [ ] Re-ranking de busca com LLM

**v4.2** (Q3 2026):
- [ ] Upgrade para qwen3.5:9b (se hardware permitir)
- [ ] Sistema de cache de análises (evitar reprocessamento)
- [ ] Análise de lote otimizada (batch API)

---

## 📚 Referências

- [Ollama Docs](https://ollama.com/docs)
- [Qwen 3.5 Release Notes](https://qwenlm.github.io/blog/qwen3.5/)
- [Nomic Embed Text](https://www.nomic.ai/blog/nomic-embed-text-v1_5-release)

---

**Modelo usado para gerar este documento**: Claude Sonnet 4.5  
**Versão do Laserflix**: v4.0.0.0
