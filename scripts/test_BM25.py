from rank_bm25 import BM25Okapi
import time
import pandas as pd
from agentic.data_loader.data_loader import load
from agentic.retriever.BM25_retriever import BM25

corpus = load("laws_de.csv")
val = load("val.csv")

retrieve_obj = BM25(corpus, val)
l = retrieve_obj.Best_Match()
print(l)