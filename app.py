"""
DKumar ONYX v3.0 — Core Engine Framework
"""
import sqlite3
from datetime import datetime

def global_intel_harvest():
    """Isolated top-level wrapper interface execution point for NVD pipeline sync."""
    import sync_engine
    sync_engine.global_intel_harvest()

class OnyxEngine:
    def __init__(self, mode="Production"):
        self.mode = mode
        self.state = {"risks": [], "total_loss": "$0.00"}

    def run(self):
        try:
            conn = sqlite3.connect("sovereign_vault.db")
            cursor = conn.cursor()
            cursor.execute("SELECT event, urgency, tech, exposure, remediation, description FROM vulnerability_intel")
            rows = cursor.fetchall()
            conn.close()
            
            self.state["risks"] = []
            total_financial = 0.0
            
            # Lazy import to stop initialization tracking crashes across secondary cores
            from predictive_engine import PredictiveRiskEngine
            pred_engine = PredictiveRiskEngine()
            
            for row in rows:
                risk_obj = {
                    "event": row[0], 
                    "urgency": row[1], 
                    "tech": row[2],
                    "exposure": row[3], 
                    "remediation": row[4], 
                    "description": row[5]
                }
                risk_obj["prediction"] = pred_engine.predict_exploitation_probability(risk_obj)
                risk_obj["velocity_score"] = risk_obj["prediction"]["velocity_score"]
                self.state["risks"].append(risk_obj)
                
                try:
                    total_financial += float(row[3].replace('$', '').replace(',', ''))
                except Exception:
                    pass
                    
            self.state["total_loss"] = f"${total_financial:,.2f}"
        except Exception:
            self.state["risks"] = []
            self.state["total_loss"] = "$0.00"

    def tool_1_intake(self, raw_log):
        conn = sqlite3.connect("sovereign_vault.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO vulnerability_intel 
            (event, urgency, tech, exposure, remediation, description) 
            VALUES (?, 'MEDIUM', 'General', '$50,000', 'Review log output.', ?)
        """, (f"ALERT-{datetime.now().strftime('%H%M%S')}", raw_log[:280]))
        conn.commit()
        conn.close()
        self.run()