import json
from neo4j import GraphDatabase

# Configuration
MATRIX_PATH = "config/regulatory_matrix.json"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "sentinel_password"

def seed_database():
    print("[*] Connecting to Neo4j Graph Database...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with open(MATRIX_PATH, "r", encoding="utf-8-sig") as f:
        matrix = json.load(f)

    with driver.session() as session:
        # 1. Clear existing database (for fresh seeding)
        session.run("MATCH (n) DETACH DELETE n")
        print("[+] Cleared existing graph.")

        # 2. Create Regulation Nodes (NIS2, EU_AI_ACT)
        for reg_key, reg_data in matrix.get("frameworks", {}).items():
            session.run(
                "CREATE (r:Regulation {name: $name, version: $version})",
                name=reg_key, version=reg_data["version"]
            )
            print(f"[+] Created Regulation Node: {reg_key}")

        # 3. Create Trigger, Article, and Relationship Edges
        for mapping in matrix.get("mappings", []):
            trigger_name = mapping["technical_trigger"]
            severity = mapping["severity"]
            remediation = mapping["standard_remediation"]

            # Create Technical Trigger Node
            session.run(
                "MERGE (t:TechnicalTrigger {id: $trigger, severity: $severity, remediation: $remediation})",
                trigger=trigger_name, severity=severity, remediation=remediation
            )

            # Link Checkov IDs to the Trigger
            for checkov_id in mapping.get("checkov_id", []):
                session.run(
                    """
                    MATCH (t:TechnicalTrigger {id: $trigger})
                    MERGE (c:CheckovID {id: $checkov_id})
                    MERGE (c)-[:TRIGGERS]->(t)
                    """,
                    trigger=trigger_name, checkov_id=checkov_id
                )

            # Create Articles and Link to Regulations and Triggers
            for link in mapping.get("regulatory_links", []):
                reg_name = link["regulation"]
                article = link["article"]
                domain = link["domain"]
                explanation = link["explanation"]

                session.run(
                    """
                    MATCH (t:TechnicalTrigger {id: $trigger})
                    MATCH (r:Regulation {name: $reg_name})
                    MERGE (a:LegalArticle {id: $article, domain: $domain})
                    MERGE (a)-[:BELONGS_TO]->(r)
                    MERGE (t)-[v:VIOLATES {explanation: $explanation}]->(a)
                    """,
                    trigger=trigger_name, reg_name=reg_name, article=article, 
                    domain=domain, explanation=explanation
                )
                print(f"[+] Mapped {trigger_name} -> {reg_name} {article}")

    driver.close()
    print("\n[SUCCESS] Neo4j XAI Compliance Graph successfully seeded!")

if __name__ == "__main__":
    seed_database()