def compute_cost_view(tenant_id: str, rules: dict):
    current_cost = 18250
    optimized = 17300
    savings = current_cost - optimized
    return {
        "optimized_cost_projection": {
            "current_month_cost_jod": current_cost,
            "optimized_cost_jod": optimized,
            "savings_jod": savings,
            "assumptions": [
                "Overtime reduced by 5%",
                "Maintenance schedule adjusted but within allowed window"
            ]
        },
        "constraints_used": rules.get("cost", [])
    }
