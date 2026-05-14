from kafka import KafkaConsumer
import subprocess
import requests
import json
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from src.graph_db.neo4j_client import ComplianceGraph
from src.semantic_engine.llama_guard import sanitize_manifest
from src.remediation.auto_patcher import generate_iac_patch

OLLAMA_URL = "http://localhost:11434/api/generate"

def emit_alert(trigger_id, regulations, status):
    try:
        requests.post("http://localhost:8000/api/v2/alert", json={
            "trigger_id": trigger_id, "regulations": regulations, "status": status
        }, timeout=1.5)
    except Exception: pass

def emit_log(source, message):
    try:
        requests.post("http://localhost:8000/api/v2/log_sink", json={"source": source, "message": str(message)}, timeout=1.5)
    except Exception: pass

def run_checkov_scan(target_dir):
    emit_log('audit', f"[*] Executing Deterministic Scanner (Checkov) on {target_dir}...")
    print(f"[*] Executing Deterministic Scanner (Checkov) on {target_dir}...")
    try:
        result = subprocess.run(['checkov', '-d', target_dir, '-o', 'json', '--quiet'], capture_output=True, text=True, shell=True)
        if not result.stdout: return []

        report = json.loads(result.stdout)
        findings = []
        reports = report if isinstance(report, list) else [report]
        
        for r in reports:
            if "results" in r and "failed_checks" in r["results"]:
                for check in r["results"]["failed_checks"]:
                    file_path = os.path.join(target_dir, check.get("file_path", "").lstrip("\\/"))
                    findings.append({"id": check["check_id"], "file": file_path})
                    
        unique_findings = [dict(t) for t in {tuple(d.items()) for d in findings}]
        return unique_findings
    except Exception as e:
        print(f"[-] Checkov Error: {e}")
        return []

def run_semantic_scan(manifest_path):
    emit_log('audit', f"[*] Initializing Sovereign Semantic Layer for {manifest_path}...")
    print(f"[*] Initializing Sovereign Semantic Layer for {manifest_path}...")
    try:
        with open(manifest_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            if not content.strip(): return []
            raw_manifest = json.loads(content)
            
        safe_manifest = sanitize_manifest(raw_manifest)
        
        prompt = f"""
        Act as an expert European IT Auditor enforcing the EU AI Act.
        Review the following software manifest. Identify if there are any unverified Generative AI dependencies or telemetry libraries that could violate data governance or supply chain security.
        Manifest: {json.dumps(safe_manifest)}
        You MUST respond ONLY with a valid JSON object containing a "violation" boolean and a "technical_trigger" string. 
        If a risk is detected, the technical_trigger MUST be exactly: "unauthenticated_third_party_api". Do not invent new trigger names.
        Example Output: {{"violation": true, "technical_trigger": "unauthenticated_third_party_api"}}
        """
        
        response = requests.post(OLLAMA_URL, json={"model": "llama3", "prompt": prompt, "stream": False, "options": {"num_ctx": 2048, "num_thread": 4, "temperature": 0.0}})
        if response.status_code != 200: return []

        llm_output = response.json().get("response", "{}")
        start_idx = llm_output.find('{')
        end_idx = llm_output.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            result = json.loads(llm_output[start_idx:end_idx + 1])
            if result.get("violation"):
                trigger_val = result.get('technical_trigger')
                emit_log('audit', f"[!] Semantic Risk Detected: {trigger_val}")
                print(f"[!] Semantic Risk Detected: {trigger_val}")
                return [trigger_val]
        return []
    except Exception as e:
        print(f"[-] Semantic Engine Error: {e}")
        return []

def run_worker():
    print("[*] Starting Sentinel-V2 Kafka Worker...")
    graph = ComplianceGraph()
    
    try:
        consumer = KafkaConsumer('sentinel-scans', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='sentinel-worker-group', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        emit_log('audit', '[+] Worker is actively listening to kafka topic...')
        print("[+] Worker is actively listening to 'sentinel-scans' topic...\n")
    except Exception as e:
        print(f"[-] Ensure Docker containers are running. Error: {e}")
        return

    for message in consumer:
        job = message.value
        print(f"\n==================================================")
        emit_log('audit', f"\n==================================================\n[*] NEW JOB RECEIVED: Scanning {job['repository_url']}")
        print(f"[*] NEW JOB RECEIVED: Scanning {job['repository_url']} (Commit: {job['commit_hash']})")
        
        target_directory = os.path.join(BASE_DIR, "dataset")
        manifest_file = os.path.join(target_directory, "package.json")
        
        all_triggers = []
        remediation_map = {}
        
        checkov_findings = run_checkov_scan(target_directory)
        if checkov_findings:
            extracted_ids = [f["id"] for f in checkov_findings]
            emit_log('audit', f"[!] Deterministic Engine flagged: {extracted_ids}")
            print(f"[!] Deterministic Engine flagged: {extracted_ids}")
            all_triggers.extend(extracted_ids)
            
        if os.path.exists(manifest_file):
            semantic_findings = run_semantic_scan(manifest_file)
            all_triggers.extend(semantic_findings)
        
        if all_triggers:
            emit_log('audit', '[*] Querying Neo4j XAI Compliance Graph...')
            print("\n[*] Querying Neo4j XAI Compliance Graph...")
            audit_report = []
            for trigger in list(set(all_triggers)):
                legal_context = graph.get_legal_context(trigger)
                if legal_context:
                    audit_report.extend(legal_context)
                    remediation_map[trigger] = legal_context
            
            # Send the JSON payload straight to the dashboard UI
            formatted_audit = json.dumps(audit_report, indent=2)
            emit_log('audit', f"[+] Explainable Audit Generation Complete:\n{formatted_audit}")
            print("[+] Explainable Audit Generation Complete:")
            print(formatted_audit)
        else:
            emit_log('audit', '[+] Pipeline secure. No compliance violations detected.')
            print("[+] Pipeline secure. No compliance violations detected.")

        if checkov_findings:
            emit_log('remediation', '[*] Initiating Autonomous Remediation Engine...\n[*] --------------------------------------------------')
            print("\n[*] --------------------------------------------------")
            print("[*] PHASE 4: Initiating Autonomous Remediation Engine...")
            for finding in checkov_findings:
                trigger_id = finding["id"]
                target_file = finding["file"]
                legal_data = remediation_map.get(trigger_id)
                
                if legal_data and os.path.exists(target_file):
                    reg_list = ", ".join(list(set([ctx.get("Regulation", "") for ctx in legal_data])))
                    emit_alert(trigger_id, reg_list, "VIOLATION_DETECTED")
                    
                    # Log the AI action to the dashboard right pane
                    emit_log('remediation', f"[*] Llama-3 rewriting {os.path.basename(target_file)} to enforce {reg_list}...")
                    generate_iac_patch(target_file, trigger_id, legal_data)
                    emit_log('remediation', f"[+] SUCCESS: {trigger_id} remediated. Code saved to {os.path.basename(target_file).replace('.tf', '_patched.tf')}\n")
                    
                    emit_alert(trigger_id, reg_list, "REMEDIATED")
                    
            emit_log('remediation', '[*] --------------------------------------------------')
            print("[*] --------------------------------------------------")
        print(f"==================================================\n")

if __name__ == "__main__":
    try:
        run_worker()
    except KeyboardInterrupt:
        print("\n[*] Shutting down worker...")
        sys.exit(0)