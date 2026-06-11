"""
DKumar ONYX v3.0 — Dynamic Regulation Mapping Engine
Maps specific CVE categories directly to cross-border frameworks.
"""

class DynamicRegulationMapper:
    # Moved the definition to be self-contained within the class or module scope
    REGULATION_CLAUSES = {
        "PIPEDA": {
            "data_exposure": "Principle 7 — Safeguards: Protect personal info against loss.",
            "authentication": "Principle 4.7.3 — Security safeguards for sensitivity.",
            "injection": "Principle 4.7 — Technical safeguards.",
            "privilege": "Principle 4.5 — Limiting use and disclosure.",
            "default": "Principle 7 — Safeguards: Protect organizational assets."
        },
        "NIST_SP_800_53": {
            "injection": "SI-10: Input Validation + SA-11: Security Testing",
            "authentication": "IA-5: Authenticator Management + AC-7: Unsuccessful Login",
            "overflow": "SI-16: Memory Protection + SC-3: Function Isolation",
            "privilege": "AC-6: Least Privilege + AU-9: Audit Protection",
            "default": "SI-2: Flaw Remediation + RA-5: Vulnerability Monitoring"
        },
        "SOX_ITGC": {"default": "Security Management — Access Control & Ops Security."},
        "PCI_DSS_v4": {"default": "Requirement 6: Maintain secure systems and assets."},
        "GDPR": {"default": "Article 32: Security of processing personal parameters."}
    }

    def _detect_category(self, text):
        mapping_rules = {
            "injection": ["injection", "sanitize", "input", "sql", "manipulation"],
            "authentication": ["authentication", "login", "handshake", "unauthenticated", "credential"],
            "overflow": ["overflow", "memory", "backdoor", "buffer", "bypass"],
            "privilege": ["privilege", "root", "unauthorized access", "compromise"]
        }
        
        text_lower = text.lower()
        for category, keywords in mapping_rules.items():
            for kw in keywords:
                if kw in text_lower:
                    return category
        return "default"

    def map_risk_to_regulations(self, risk):
        # Ensure 'risk' is a dictionary to prevent AttributeErrors
        desc = f"{risk.get('event','')} {risk.get('description','')} {risk.get('tech','')}".lower()
        severity = risk.get('urgency', 'MEDIUM').upper()
        category = self._detect_category(desc)

        violations = {}
        for fw, clauses in self.REGULATION_CLAUSES.items():
            clause = clauses.get(category, clauses["default"])
            
            # Risk Escalation Rule
            if severity in ["CRITICAL", "HIGH"]:
                breach_risk = "HIGH"
            elif severity == "MEDIUM":
                breach_risk = "MEDIUM"
            else:
                breach_risk = "LOW"
                
            violations[fw] = {"clause": clause, "breach_risk": breach_risk}
        return violations