"""
Test and demonstration script for the production RAG chunking pipeline.

This script demonstrates:
1. Loading raw datasets
2. Running semantic chunking on laws
3. Running hierarchical chunking on court decisions
4. Saving results
5. Basic retrieval examples

Run this from project root:
    python scripts/demo_chunking_pipeline.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agentic.pipeline.rag_orchestrator import (
    RAGPipelineOrchestrator,
    RetrievalInterface
)
from agentic.data_loader import load


def demo_laws_chunking():
    """Demonstrate laws chunking on a small sample."""
    print("\n" + "="*70)
    print("DEMO 1: Laws Dataset Semantic Chunking")
    print("="*70)
    
    # Load small sample
    laws_df = load(filename="laws_de.csv", nrows=10)
    print(f"Loaded {len(laws_df)} laws records")
    
    # Initialize orchestrator
    orchestrator = RAGPipelineOrchestrator()
    
    # Chunk laws
    laws_chunks = orchestrator.chunk_laws(laws_df)
    
    print(f"\nGenerated {len(laws_chunks)} chunks from {len(laws_df)} laws")
    print("\nSample chunks:")
    
    for idx, row in laws_chunks.head(3).iterrows():
        print(f"\n  Citation: {row['citation']}")
        print(f"  Article: {row['article']}")
        print(f"  Tokens: {row['tokens']}")
        print(f"  Type: {row['chunk_type']}")
        print(f"  Text (first 150 chars): {row['text'][:150]}...")


def demo_court_chunking():
    """Demonstrate court decisions chunking on a small sample."""
    print("\n" + "="*70)
    print("DEMO 2: Court Decisions Hierarchical Chunking")
    print("="*70)
    
    # Load small sample
    court_df = load(filename="court_considerations.csv", nrows=5)
    print(f"Loaded {len(court_df)} court decision records")
    
    # Initialize orchestrator
    orchestrator = RAGPipelineOrchestrator()
    
    # Chunk court decisions
    court_chunks = orchestrator.chunk_court_decisions(court_df)
    
    print(f"\nGenerated {len(court_chunks)} chunks from {len(court_df)} court decisions")
    print("\nSample chunks:")
    
    for idx, row in court_chunks.head(3).iterrows():
        print(f"\n  Citation: {row['citation']}")
        print(f"  Section: {row['section']}")
        print(f"  Tokens: {row['tokens']}")
        print(f"  Type: {row['chunk_type']}")
        print(f"  Text (first 150 chars): {row['text'][:150]}...")


def demo_full_pipeline():
    """Demonstrate the complete end-to-end pipeline."""
    print("\n" + "="*70)
    print("DEMO 3: Full End-to-End RAG Pipeline")
    print("="*70)
    
    orchestrator = RAGPipelineOrchestrator()
    
    # Run complete pipeline with small sample
    report = orchestrator.run_full_pipeline(
        laws_nrows=100,
        court_nrows=500,
        save_format="parquet"
    )
    
    print("\nPipeline Report:")
    print(f"  Total Chunks: {report['total_chunks']}")
    print(f"  Total Tokens: {report['total_tokens']}")
    print(f"  Duration: {report['duration_seconds']:.2f} seconds")
    print(f"  Laws Chunks: {report['output_chunks']['laws']['num_chunks']}")
    print(f"  Court Chunks: {report['output_chunks']['court_decisions']['num_chunks']}")


def demo_retrieval():
    """Demonstrate retrieval interface."""
    print("\n" + "="*70)
    print("DEMO 4: Chunk Retrieval Interface")
    print("="*70)
    
    orchestrator = RAGPipelineOrchestrator()
    
    # Load small sample
    laws_df = load(filename="laws_de.csv", nrows=20)
    laws_chunks = orchestrator.chunk_laws(laws_df)
    
    # Create retrieval interface
    retriever = RetrievalInterface(laws_chunks)
    
    # Demo 1: Get chunks by source type
    law_chunks = retriever.get_chunks_for_source('law')
    print(f"\nTotal law chunks: {len(law_chunks)}")
    
    # Demo 2: Get chunks by token range
    medium_chunks = retriever.get_by_token_range(100, 200)
    print(f"Chunks with 100-200 tokens: {len(medium_chunks)}")
    
    # Demo 3: Text search
    if len(laws_chunks) > 0:
        first_citation = laws_chunks.iloc[0]['citation']
        citation_chunks = retriever.get_by_citation(first_citation)
        print(f"Chunks for citation '{first_citation}': {len(citation_chunks)}")
    
    print("\nRetrieval interface ready for use in RAG!")


def demo_chunking_stats():
    """Show detailed chunking statistics."""
    print("\n" + "="*70)
    print("DEMO 5: Chunking Statistics")
    print("="*70)
    
    orchestrator = RAGPipelineOrchestrator()
    
    # Load and chunk small sample
    laws_df = load(filename="laws_de.csv", nrows=50)
    laws_chunks = orchestrator.chunk_laws(laws_df)
    
    stats = orchestrator.pipeline.get_chunking_stats(laws_chunks)
    
    print("\nLaws Chunking Statistics:")
    print(f"  Total Chunks: {stats['total_chunks']}")
    print(f"  Total Tokens: {stats['total_tokens']}")
    print(f"  Average Tokens per Chunk: {stats['avg_tokens_per_chunk']:.2f}")
    print(f"  Min Tokens: {stats['min_tokens']}")
    print(f"  Max Tokens: {stats['max_tokens']}")
    print(f"  Chunks < 50 tokens: {stats['chunks_below_threshold']}")
    print(f"  Chunks > 500 tokens: {stats['chunks_above_threshold']}")
    
    # Chunk court for comparison
    court_df = load(filename="court_considerations.csv", nrows=10)
    court_chunks = orchestrator.chunk_court_decisions(court_df)
    
    stats_court = orchestrator.pipeline.get_chunking_stats(court_chunks)
    
    print("\nCourt Decisions Chunking Statistics:")
    print(f"  Total Chunks: {stats_court['total_chunks']}")
    print(f"  Total Tokens: {stats_court['total_tokens']}")
    print(f"  Average Tokens per Chunk: {stats_court['avg_tokens_per_chunk']:.2f}")
    print(f"  Min Tokens: {stats_court['min_tokens']}")
    print(f"  Max Tokens: {stats_court['max_tokens']}")


def main():
    """Run all demonstrations."""
    print("\n" + "#"*70)
    print("# RAG Production Chunking Pipeline - Demonstration")
    print("#"*70)
    
    try:
        # Run demos
        demo_laws_chunking()
        demo_court_chunking()
        demo_chunking_stats()
        demo_full_pipeline()
        demo_retrieval()
        
        print("\n" + "#"*70)
        print("# All demonstrations completed successfully!")
        print("#"*70 + "\n")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
