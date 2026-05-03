from agentic.retriever.create_index import create_unified_corpus
from agentic.data_loader.data_loader import load

law_df = load("laws_de.csv", nrows = 1000)
court_df = load("court_considerations.csv", nrows = 1000)

create_unified_corpus(law_df, court_df)