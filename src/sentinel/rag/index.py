
"""Vector index of the policies (ChromaDB, stored locally as files)."""

import shutil
from pathlib import Path

import chromadb

from sentinel.rag.policies import Policy

COLLECTION = "policies"


def build_policy_index(policies: list[Policy], index_dir: Path) -> int:
    """Rebuild the index from scratch; return how many policies were stored."""
    shutil.rmtree(index_dir, ignore_errors=True)
    client = chromadb.PersistentClient(path=str(index_dir))
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=[p.policy_id for p in policies],
        documents=[f"{p.title}. {p.text}" for p in policies],
        metadatas=[{"title": p.title} for p in policies],
    )
    return collection.count()


def retrieve_policies(case: str, index_dir: Path, k: int = 3) -> list[dict]:
    """Return the k policies closest in meaning to the case description."""
    client = chromadb.PersistentClient(path=str(index_dir))
    collection = client.get_collection(COLLECTION)
    result = collection.query(query_texts=[case], n_results=k)
    return [
        {"policy_id": pid, "title": meta["title"], "text": doc, "distance": dist}
        for pid, doc, meta, dist in zip(
            result["ids"][0], result["documents"][0],
            result["metadatas"][0], result["distances"][0],
        )
    ]
