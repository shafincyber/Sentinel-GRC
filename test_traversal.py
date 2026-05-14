import json
from src.graph_db.neo4j_client import ComplianceGraph

def test_graph_traversal():
    print("[*] Initializing XAI Graph Traversal...")
    graph = ComplianceGraph()
    
    # Simulate Checkov finding an unencrypted S3 bucket
    simulated_checkov_flag = "CKV_AWS_19"
    print(f"[*] Simulating Checkov output: {simulated_checkov_flag}")
    
    # Query the graph
    print("[*] Traversing Graph for Legal Context...\n")
    legal_context = graph.get_legal_context(simulated_checkov_flag)
    
    if legal_context:
        print(json.dumps(legal_context, indent=4))
        print("\n[+] SUCCESS: Deterministic Legal Mapping Retrieved!")
    else:
        print("\n[-] FAILED: No mapping found in graph.")
        
    graph.close()

if __name__ == "__main__":
    test_graph_traversal()