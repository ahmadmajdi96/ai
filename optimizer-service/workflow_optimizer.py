def compute_workflow_view(tenant_id: str, rules: dict):
    critical_path_steps = ["Filling", "Capping", "Labeling", "Packing"]
    return {
        "critical_path_steps": critical_path_steps,
        "longest_path_minutes": 42,
        "recommended_change": "Move QC inline between Capping and Labeling",
        "expected_cycle_time_improvement_min": 5
    }
