# Agentic-Retrieval-Competition

[LLM Agentic Legal Information Retrieval](https://www.kaggle.com/competitions/llm-agentic-legal-information-retrieval)

This project implements a complete retrieval-augmented generation (RAG) pipeline for the Kaggle competition on Swiss legal citation retrieval.

## Features

- Hybrid retrieval combining BM25, FAISS dense retrieval, and regex matching
- Query expansion using Qwen2.5 LLM
- Two-stage reranking with MiniLM and BGE models
- Unified corpus indexing for laws and court considerations
- Production-ready chunking and embedding pipelines

## Setup

### Prerequisites

- Python 3.10+
- Git (for cloning if needed)

### Installation

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd Agentic-Retrieval-Competition
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or for development:
   ```bash
   pip install -e .
   ```

### Data Preparation

Ensure the following data files are in the `data/` directory:
- `laws_de.csv` - Swiss legal texts
- `court_considerations.csv` - Court consideration texts
- `val.csv` - Validation queries

## Usage

### Running the Full Pipeline

To run the complete RAG pipeline on all validation queries:

```bash
python scripts/run_pipeline.py
```

This will:
- Load and preprocess all data
- Build FAISS indexes (takes several minutes)
- Process all queries with hybrid retrieval and reranking
- Save results to `artifacts/submission.csv`

### Testing Individual Components

Test specific components using the provided scripts:

```bash
# Test FAISS retrieval
python scripts/test_faiss.py

# Test BM25 retrieval
python scripts/test_BM25.py

# Test query expansion
python scripts/test_query_expansion.py

# Test chunking pipeline
python scripts/test_chunking.py
```

## Configuration

Modify `config/config.yaml` to adjust:
- Model parameters
- Retrieval settings
- Logging levels

## Troubleshooting

### SSL Certificate Issues

If you encounter SSL errors with Hugging Face models:

```bash
unset SSL_CERT_FILE
```

Or in PowerShell:
```powershell
$env:SSL_CERT_FILE = ""
```

### Memory Issues

The pipeline requires significant RAM for model loading and indexing. Ensure at least 16GB RAM is available.

### GPU Acceleration

For faster processing, ensure CUDA-compatible GPU is available. The pipeline will automatically use GPU if detected.

## Project Structure

```
├── src/agentic/           # Main package
│   ├── pipeline/         # RAG pipeline implementation
│   ├── retriever/        # Retrieval components
│   ├── models/           # LLM and expansion models
│   ├── embeddings/       # Embedding utilities
│   └── ...
├── scripts/              # Executable scripts
├── data/                 # Dataset files
├── config/               # Configuration files
├── artifacts/            # Output directory
└── logs/                 # Log files
```

## License

MIT License - see LICENSE file for details.