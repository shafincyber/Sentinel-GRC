import requests
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_iac_patch(target_file, trigger_id, legal_context):
    """
    Uses the local Sovereign LLM to rewrite vulnerable code strictly based on Neo4j Graph mandates.
    Dynamically supports Terraform and Kubernetes (YAML) manifests.
    """
    print(f"\n[*] Initiating Autonomous Remediation for: {trigger_id}")
    print(f"[*] Target File: {target_file}")
    
    if not os.path.exists(target_file):
        print("[-] Error: Target IaC file not found.")
        return False

    with open(target_file, 'r', encoding='utf-8') as f:
        vulnerable_code = f.read()

    # Extract dynamic compliance data from the Neo4j graph object
    regulations = ", ".join(list(set([ctx.get("Regulation", "") for ctx in legal_context])))
    articles = ", ".join(list(set([ctx.get("Article", "") for ctx in legal_context])))
    remediation_mandate = legal_context[0].get("Remediation", "Implement secure architecture.")

    # Determine IaC Type to focus the LLM
    is_yaml = target_file.endswith(('.yaml', '.yml'))
    lang_block = "yaml" if is_yaml else "terraform"
    iac_type = "Kubernetes Manifest" if is_yaml else "Terraform"

    print(f"[*] Engine Context: {iac_type}")
    print(f"[*] Enforcing mandates for: {regulations} | {articles}")

    prompt = f"""
    Act as a deterministic DevSecOps Autonomous Agent.
    Your task is to remediate a {iac_type} vulnerability to ensure strict compliance with European Law.
    
    VULNERABILITY ID: {trigger_id}
    GOVERNING LAWS: {regulations}
    LEGAL ARTICLES: {articles}
    REQUIRED REMEDIATION MANDATE: {remediation_mandate}
    
    VULNERABLE CODE:
    ```{lang_block}
    {vulnerable_code}
    ```
    
    INSTRUCTIONS:
    1. Rewrite the code strictly to implement the REQUIRED REMEDIATION MANDATE.
    2. Do NOT change resource names, metadata, namespaces, or any unrelated variables.
    3. Output ONLY the raw, perfectly formatted code. 
    4. Do NOT include markdown blocks (like ```{lang_block}).
    5. Do NOT include any conversational text, explanations, or greetings.
    """

    print("[*] Generating legally-compliant patch via Llama-3...")
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False, 
            "options": {"num_ctx": 4096, "num_thread": 4, "temperature": 0.0}
        })
        
        if response.status_code != 200:
            print(f"[-] AI Engine Failure: {response.status_code}")
            return False

        patched_code = response.json().get("response", "").strip()

        if patched_code.startswith("```"):
            patched_code = "\n".join(patched_code.split("\n")[1:])
        if patched_code.endswith("```"):
            patched_code = "\n".join(patched_code.split("\n")[:-1])

        patched_file_path = target_file.replace(".tf", "_patched.tf").replace(".yaml", "_patched.yaml").replace(".yml", "_patched.yml")
        with open(patched_file_path, 'w', encoding='utf-8') as f:
            f.write(patched_code)
            
        print(f"[+] SUCCESS: Patched infrastructure saved to -> {patched_file_path}")
        return True

    except Exception as e:
        print(f"[-] Remediation Error: {e}")
        return False
