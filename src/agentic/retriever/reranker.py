from sentence_transformers import CrossEncoder

# Load CrossEncoder model for reranker
reranker = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', max_length=512)
