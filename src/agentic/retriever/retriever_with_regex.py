from agentic.exception import Agentic_Exception
import sys

# Building the Rule base Extractor pipeline
def extract_and_clean_citations(text) :
    """
    Agent Tool: This function extract the citation from the query text using Regex pattern
    """
    if not isinstance(text, str) :
        return []

    # Polish pattern for extract the citation
    pattern = r"Art\.\s*\d+(?:\s+(?:Abs\.|lit\.|Ziff\.)\s+[a-z0-9]+)*\s+[A-Za-z]+"

    # Finding the matching citation
    raw_matches = re.findall(pattern, text)

    cleaned_citations = set()
    try :
        for match in raw_matches :
            clean_cit = re.sub(r'\s+lit\.\s+[a-z]+', '', match)
            clean_cit = re.sub(r'\s+Ziff\.\s+\d+', '', clean_cit)

            # Clean up any extra spaces
            clean_cit = " ".join(clean_cit.split())
            cleaned_citations.add(clean_cit)
        return list(cleaned_citations)
    except Exception as e :
        raise Agentic_Exception(e, sys) from e


for index, row in val_df.iterrows():
    query_text = row['query']
    
    # Handle possible NaN values in gold_citations
    gold_str = str(row['gold_citations']) if pd.notnull(row['gold_citations']) else ""
    gold_cits = set(gold_str.split(';')) if gold_str else set()
    
    # Extract using our new tool
    extracted_cits = set(extract_and_clean_citations(query_text))
    
    # Calculate hits
    hits = extracted_cits.intersection(gold_cits)
    
    total_gold += len(gold_cits)
    total_extracted += len(extracted_cits)
    total_hits += len(hits)