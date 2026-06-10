import chromadb
from sentence_transformers import SentenceTransformer

from ingest import load_and_chunk_documents

COLLECTION_NAME = "professor_reviews"
TOP_K = 5

# Load once at import time so every retrieve() call reuses the same model
_model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store(docs_dir: str = "documents") -> chromadb.Collection:
    """Embed all chunks and load them into a local ChromaDB collection."""
    chunks = load_and_chunk_documents(docs_dir)

    texts = [c["text"] for c in chunks]
    embeddings = _model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path="chroma_db")

    # Delete existing collection so re-runs start fresh
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"], "chunk_index": i} for i, c in enumerate(chunks)],
    )

    print(f"Stored {collection.count()} chunks in ChromaDB collection '{COLLECTION_NAME}'.")
    return collection


def get_collection() -> chromadb.Collection:
    """Load the existing ChromaDB collection (must call build_vector_store first)."""
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection(COLLECTION_NAME)


def retrieve(query: str, collection: chromadb.Collection, k: int = TOP_K) -> list[dict]:
    """Return the top-k most relevant chunks for a query with source and distance."""
    query_embedding = _model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta["source"], "distance": round(dist, 4)})
    return chunks


if __name__ == "__main__":
    collection = build_vector_store()

    test_queries = [
        "Which CS professor is the best for discrete math?",
        "Who is better for Computer Architecture, Shankar or Shostak?",
        "Which professor is the worst for CSCI 335?",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("="*60)
        results = retrieve(query, collection)
        for i, chunk in enumerate(results, 1):
            print(f"\n  [{i}] Source: {chunk['source']}  |  Distance: {chunk['distance']}")
            print(f"      {chunk['text'][:250]}")
