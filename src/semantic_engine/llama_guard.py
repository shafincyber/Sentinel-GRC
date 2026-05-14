def sanitize_manifest(manifest_json):
    print("[*] Passing manifest through Llama Guard Prompt Firewall...")
    # Placeholder: Logic to detect prompt overrides before hitting the main LLM
    forbidden_strings = ["ignore previous instructions", "override", "system prompt"]
    
    manifest_string = str(manifest_json).lower()
    for threat in forbidden_strings:
        if threat in manifest_string:
            raise ValueError(f"CRITICAL: Prompt Injection Signature Detected -> '{threat}'")
    
    print("[+] Manifest sanitized successfully.")
    return manifest_json
