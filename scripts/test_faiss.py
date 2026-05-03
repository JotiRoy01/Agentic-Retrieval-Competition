from agentic.retriever.faiss_retriever import Faiss
from agentic.data_loader.data_loader import load
from agentic.models.expansion_query import QueryExpansion


law = load("laws_de.csv", nrows = 1000)
val = load("val.csv")


expansion_class = QueryExpansion()
generated_text = expansion_class.Eng_plus_Germ()
llm_german_keywords = generated_text.strip()

#expanded_query = f"{test_query} {llm_german_keywords}"
test_query = val['query'].iloc[0]
expanded_query = f"{test_query} {llm_german_keywords}"
print(f"expanded_query: \n{expanded_query}")



f = Faiss(law, expanded_query)

full_dense_score, full_dense_indices = f.Faiss_retriever()

print(f"ful_dense_score: {full_dense_score} \nfull_dense_indices: {full_dense_indices}")