import pytest
import sys
import os

# Ensure the test suite can find the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.graph_db.neo4j_client import ComplianceGraph

@pytest.fixture(scope="module")
def graph_client():
    print("\n[*] Initializing Neo4j Graph Connection for Testing...")
    graph = ComplianceGraph()
    yield graph
    graph.close()
    print("\n[*] Closed Neo4j Graph Connection.")

def test_unencrypted_storage_mapping(graph_client):
    """Test if unencrypted_data_at_rest correctly maps to GDPR and NIS2."""
    context = graph_client.get_legal_context("unencrypted_data_at_rest")
    assert len(context) > 0, "No context returned for unencrypted_data_at_rest"
    regulations = [c["Regulation"] for c in context]
    assert "GDPR" in regulations, "GDPR mapping missing"
    assert "NIS2" in regulations, "NIS2 mapping missing"

def test_unauthenticated_api_mapping(graph_client):
    """Test if unauthenticated_third_party_api maps to all 3 frameworks."""
    context = graph_client.get_legal_context("unauthenticated_third_party_api")
    assert len(context) > 0, "No context returned for unauthenticated_third_party_api"
    regulations = [c["Regulation"] for c in context]
    assert "GDPR" in regulations
    assert "NIS2" in regulations
    assert "EU_AI_ACT" in regulations

def test_checkov_id_traversal(graph_client):
    """Test if a raw Checkov ID (CKV_K8S_16) successfully traverses to the trigger and then to the law."""
    context = graph_client.get_legal_context("CKV_K8S_16")
    assert len(context) > 0, "Traversal failed for CKV_K8S_16"
    regulations = [c["Regulation"] for c in context]
    assert "NIS2" in regulations

def test_invalid_trigger_returns_empty(graph_client):
    """Ensure hallucinated or invalid triggers return empty lists, not false positives."""
    context = graph_client.get_legal_context("NON_EXISTENT_TRIGGER_999")
    assert len(context) == 0, "False positive detected on invalid trigger!"
