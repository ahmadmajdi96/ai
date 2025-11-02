def compute_risk_view(tenant_id: str, rules: dict):
    return {
        "top_risks": [
            {
                "risk": "Skipping calibration",
                "severity": "high",
                "impact": "Increased scrap rate and downtime"
            },
            {
                "risk": "Supplier B viscosity variance",
                "severity": "medium",
                "impact": "Micro-stops in filler station"
            }
        ]
    }
