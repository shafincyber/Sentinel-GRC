from neo4j import GraphDatabase

class ComplianceGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="sentinel_password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_legal_context(self, trigger_id):
        """
        Traverses the graph starting from EITHER a Checkov ID or a Semantic Technical Trigger.
        """
        query = """
        MATCH (t:TechnicalTrigger)
        WHERE t.id = $trigger_id OR EXISTS { MATCH (c:CheckovID {id: $trigger_id})-[:TRIGGERS]->(t) }
        MATCH (t)-[v:VIOLATES]->(a:LegalArticle)
        MATCH (a)-[:BELONGS_TO]->(r:Regulation)
        RETURN 
            r.name AS Regulation, 
            a.id AS Article, 
            a.domain AS Domain,
            t.severity AS Severity,
            v.explanation AS Explanation,
            t.remediation AS Remediation
        """
        with self.driver.session() as session:
            result = session.run(query, trigger_id=trigger_id)
            return [record.data() for record in result]

if __name__ == "__main__":
    print("[*] Sentinel-V2 Compliance Graph Client Ready.")