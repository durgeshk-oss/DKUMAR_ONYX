"""
DKumar ONYX v3.0 — Predictive Risk Engine
30/60/90 day exploitation probability forecasting — Stabilized Logic Passed
"""
from datetime import datetime

class PredictiveRiskEngine:
    EXPLOIT_VELOCITY = {
        "injection": 7, "overflow": 14, "authentication": 10,
        "privilege": 21, "information": 45, "default": 30
    }
    TECH_EXPOSURE_MULTIPLIER = {
        "Apache": 2.1, "Tomcat": 1.8, "Windows": 1.5,
        "MySQL": 1.3, "Linux": 1.2, "Java": 1.1, "General": 1.0
    }

    def predict_exploitation_probability(self, risk):
        # FIX: Cross-examine both 'description' and 'event' fields to capture vulnerability categories cleanly
        event_str = risk.get('event', '').lower()
        desc_str  = risk.get('description', '').lower()
        combined_context = f"{event_str} {desc_str}"

        tech     = risk.get('tech', 'General')
        severity = risk.get('urgency', 'MEDIUM').upper()

        base_prob = {"CRITICAL": 0.85, "HIGH": 0.55, "MEDIUM": 0.25, "LOW": 0.08}.get(severity, 0.25)

        category = "default"
        for cat in self.EXPLOIT_VELOCITY:
            if cat in combined_context:
                category = cat
                break

        days_to_exploit = self.EXPLOIT_VELOCITY[category]
        tech_mult       = self.TECH_EXPOSURE_MULTIPLIER.get(tech, 1.0)

        predictions = {}
        for days in [30, 60, 90]:
            time_factor = min(1.0, days / days_to_exploit)
            adjusted    = base_prob * tech_mult * time_factor
            predictions[f"{days}d"] = round(min(0.99, adjusted), 3)

        velocity_score = int((base_prob * tech_mult * (30 / days_to_exploit)) * 100)

        return {
            "base_probability": base_prob,
            "predictions": predictions,
            "velocity_score": min(100, velocity_score),
            "recommended_patch_window": f"{days_to_exploit} days",
            "category": category
        }

    def rank_by_predicted_impact(self, risks):
        scored = []
        for risk in risks:
            prediction = self.predict_exploitation_probability(risk)
            risk = dict(risk)
            risk['prediction'] = prediction
            try:
                exp_val = float(risk.get('exposure', '$0').replace('$', '').replace(',', '') or 0)
            except Exception:
                exp_val = 0
            risk['composite_score'] = (
                prediction['velocity_score'] * 0.4 +
                exp_val / 10000 * 0.6
            )
            scored.append(risk)
        return sorted(scored, key=lambda x: x['composite_score'], reverse=True)