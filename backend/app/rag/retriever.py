"""
Retriever simples baseado em palavras-chave.

Isso representa a camada de "recuperação" de um pipeline RAG.
A interface (retrieve(query, top_k)) é a mesma que você usaria com
um vector store de verdade (Chroma/FAISS + embeddings) — então dá
pra evoluir esse arquivo sem tocar no resto do agente.
"""

from app.data.study_content import STUDY_CONTENT


def _score(query: str, item: dict) -> int:
    query_words = set(query.lower().split())
    haystack = set(item["keywords"]) | {item["domain"].lower()} | set(
        item["topic"].lower().split()
    )
    return len(query_words & haystack)


def retrieve(query: str, domain: str | None = None, top_k: int = 3) -> list[dict]:
    """
    Busca os `top_k` trechos de conteúdo mais relevantes para a query.
    Se `domain` for informado, filtra apenas aquele domínio da prova.
    """
    candidates = STUDY_CONTENT
    if domain:
        candidates = [c for c in candidates if c["domain"].lower() == domain.lower()]

    scored = [(_score(query, item), item) for item in candidates]
    scored.sort(key=lambda pair: pair[0], reverse=True)

    # Se nada bateu por keyword, devolve os primeiros do domínio (fallback)
    results = [item for score, item in scored if score > 0][:top_k]
    if not results:
        results = candidates[:top_k]

    return results
