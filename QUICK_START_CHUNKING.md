# Quick Start Guide: Production RAG Chunking Pipeline

## 1. Setup (2 minutes)

```bash
# Navigate to project root
cd /path/to/Agentic-Retrieval-Competition

# Requirements already satisfied (uses existing pandas, yaml, etc.)
# No additional dependencies needed!
```

## 2. Run Demo (3 minutes)

```bash
# From project root
python scripts/demo_chunking_pipeline.py
```

Expected output:
```
=====================================================================
DEMO 1: Laws Dataset Semantic Chunking
=====================================================================
Loaded 10 laws records
Chunking 10 laws records (semantic strategy)...
Generated 47 chunks from 10 laws
Laws chunking stats: {...}

Sample chunks:
  Citation: Art. 1 112
  Article: Art. 1
  Tokens: 245
  ...
```

## 3. Production Pipeline (30 seconds)

```python
# In your script or notebook
from agentic.pipeline.rag_orchestrator import run_production_chunking_pipeline

# Run complete pipeline (on full dataset)
report = run_production_chunking_pipeline(
    laws_file="laws_de.csv",
    court_file="court_considerations.csv"
)

print(f"✅ Generated {report['total_chunks']} chunks")
print(f"📊 Total tokens: {report['total_tokens']}")
```

## 4. Test with Small Sample (1 minute)

```python
from agentic.pipeline.rag_orchestrator import RAGPipelineOrchestrator

orchestrator = RAGPipelineOrchestrator()

# Test on small sample
report = orchestrator.run_full_pipeline(
    laws_nrows=100,      # Only 100 laws for testing
    court_nrows=500,     # Only 500 court decisions
    save_format="parquet"
)

print(f"✅ Test complete: {report['total_chunks']} chunks generated")
```

## 5. Use Chunks in Your RAG

```python
from agentic.pipeline.rag_orchestrator import RetrievalInterface

# Load pre-computed chunks
import pandas as pd
chunks = pd.read_parquet("artifacts/chunks/laws_chunks.parquet")

# Create retriever
retriever = RetrievalInterface(chunks)

# Example queries
art_1_chunks = retriever.get_by_citation("Art. 1 112")
relevant_chunks = retriever.search_text("Grundstück")

# Ready for embedding model!
texts = relevant_chunks['text'].tolist()
```

## Key Features at a Glance

| Feature | Details |
|---------|---------|
| **Laws Chunking** | 100-300 tokens, semantic chunks by article |
| **Court Chunking** | 200-500 tokens, hierarchical by decision sections |
| **Metadata** | Citation, section, token count preserved |
| **Output** | Parquet (fast) or CSV (portable) |
| **Memory** | ~2-3GB for laws, ~5-8GB for court decisions |
| **Time** | ~10 mins laws, ~60 mins court (full dataset) |

## Common Tasks

### Get Chunking Statistics
```python
orchestrator = RAGPipelineOrchestrator()
laws_chunks = orchestrator.chunk_laws(laws_df)
stats = orchestrator.pipeline.get_chunking_stats(laws_chunks)
```

### Save to Different Format
```python
# Save as CSV instead of Parquet
orchestrator.save_chunks(chunks, "my_chunks", format="csv")
```

### Process in Batches
```python
# For very large datasets
laws_df_1 = orchestrator.load_laws_dataset("laws_de.csv", nrows=50000)
laws_chunks_1 = orchestrator.chunk_laws(laws_df_1)
orchestrator.save_chunks(laws_chunks_1, "laws_chunks_part_1")

laws_df_2 = orchestrator.load_laws_dataset("laws_de.csv", nrows=50000, skip_rows=50000)
laws_chunks_2 = orchestrator.chunk_laws(laws_df_2)
orchestrator.save_chunks(laws_chunks_2, "laws_chunks_part_2")
```

## Architecture Overview

```
┌─────────────────────┐
│  Raw CSV Data       │
│ laws_de.csv         │
│ court_***.csv       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  DataLoader (existing)                  │
│  Loads CSV files                        │
└──────────┬──────────────────────────────┘
           │
           ├─────────────┬────────────────┐
           ▼             ▼                ▼
    ┌──────────────────────────────────────┐
    │  ProductionChunkingPipeline          │
    ├──────────────────────────────────────┤
    │  LawsSemanticChunker                 │
    │  • Article-based splitting           │
    │  • Subsection preservation           │
    │  • 100-300 tokens per chunk          │
    │                                      │
    │  CourtHierarchicalChunker            │
    │  • Decision section splitting        │
    │  • Hierarchy preservation            │
    │  • 200-500 tokens per chunk          │
    └──────────┬───────────────────────────┘
           │
           ▼
    ┌──────────────────────┐
    │  Chunked DataFrames  │
    │  + Metadata          │
    └──────────┬───────────┘
           │
           ▼
    ┌──────────────────────────┐
    │  Save (Parquet/CSV)      │
    │  artifacts/chunks/       │
    └──────────┬───────────────┘
           │
           ▼
    ┌────────────────────────────────────┐
    │  RetrievalInterface                │
    │  • get_by_citation()               │
    │  • get_by_section()                │
    │  • search_text()                   │
    │  • get_by_token_range()            │
    └────────────────────────────────────┘
           │
           ▼
    ┌──────────────────────────┐
    │  Vector Store / RAG      │
    │  (Next step)             │
    └──────────────────────────┘
```

## Troubleshooting

**Q: Pipeline takes too long?**
A: Process in batches with `nrows` parameter
```python
orchestrator.load_laws_dataset("laws_de.csv", nrows=100000)
```

**Q: Out of memory?**
A: Use smaller `nrows` or more RAM
```python
laws_df = orchestrator.load_laws_dataset("laws_de.csv", nrows=50000)
```

**Q: Chunks too small/large?**
A: Adjust thresholds in chunker initialization
```python
from agentic.chunkings.production_chunker import LawsSemanticChunker
chunker = LawsSemanticChunker(target_tokens=250, max_tokens=350, min_tokens=75)
```

## Next Steps

1. ✅ **Chunking** - You are here!
2. **Embedding** - Encode chunks with embedding model
3. **Vector Store** - Store embeddings (Pinecone, Milvus, Weaviate)
4. **Retrieval** - Build BM25 + semantic retrieval
5. **Generation** - Use LLM with retrieved context

## File Locations

| File | Purpose |
|------|---------|
| `src/agentic/chunkings/production_chunker.py` | Core chunking logic |
| `src/agentic/pipeline/rag_orchestrator.py` | Orchestration & retrieval |
| `scripts/demo_chunking_pipeline.py` | Demonstration script |
| `artifacts/chunks/` | Output chunks location |
| `RAG_CHUNKING_GUIDE.md` | Full documentation |

## Support

- **Detailed Guide**: See `RAG_CHUNKING_GUIDE.md`
- **Demo Script**: Run `python scripts/demo_chunking_pipeline.py`
- **Logs**: Check `pipeline_report.json` in artifacts/

---

**Ready?** → `python scripts/demo_chunking_pipeline.py`
