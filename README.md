# Agentic-Retrieval-Competition
[LLM Agentic Legal Information Retrieval](https://www.kaggle.com/competitions/llm-agentic-legal-information-retrieval)
This project completed based on kaggle competition LLM Agentic Legal Information Retrieval.

The crash is from httpx/huggingface_hub trying to build an SSL context using SSL_CERT_FILE, and that env var points to a file that does not exist.

```bash
unset SSL_CERT_FILE
python scripts/test_faiss.py
```
Alternative: PowerShell
If you are on Windows and prefer PowerShell, you can use
```bash
Get-ChildItem -Recurse | Select-Object FullName
```
Once you have the output, you can copy and paste it into our chat