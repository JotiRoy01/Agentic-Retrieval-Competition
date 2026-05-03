# Agentic-Retrieval-Competition
This project completed based on kaggle competition LLM Agentic Legal Information Retrieval.

The crash is from httpx/huggingface_hub trying to build an SSL context using SSL_CERT_FILE, and that env var points to a file that does not exist.

```bash
unset SSL_CERT_FILE
python scripts/test_faiss.py
```