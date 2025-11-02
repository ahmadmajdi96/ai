def compute_bottleneck_view(tenant_id: str, rules: dict):
    return {
        "primary_bottleneck": {
            "line": "Packaging Line 2",
            "utilization_pct": 92,
            "reason": "Extended changeover time",
            "impact_units_per_shift": 480
        },
        "suggested_action": "Run SMED and retrain changeover team"
    }
