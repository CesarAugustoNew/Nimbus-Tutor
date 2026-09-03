import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.retriever import retrieve


def test_retrieve_finds_relevant_content_by_keyword():
    results = retrieve(query="iam usuarios permissoes")
    assert len(results) > 0
    assert any("IAM" in r["topic"] for r in results)


def test_retrieve_filters_by_domain():
    results = retrieve(query="qualquer coisa", domain="Billing, Pricing and Support")
    assert len(results) > 0
    assert all(r["domain"] == "Billing, Pricing and Support" for r in results)


def test_retrieve_has_fallback_when_no_keyword_matches():
    results = retrieve(query="palavra que nao existe em lugar nenhum xyz123")
    assert len(results) > 0  # fallback não deve retornar lista vazia
