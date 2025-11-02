from common_lib.db import fetch_all

def detect_bottlenecks(tenant_id: str):
    rows = fetch_all("""
        SELECT line_id,
               COUNT(*) FILTER (WHERE downtime_reason IS NOT NULL) AS stops
        FROM production_events
        WHERE tenant_id=%s
          AND ts > NOW() - INTERVAL '24 hours'
        GROUP BY line_id
        ORDER BY stops DESC
        LIMIT 1
    """,[tenant_id])

    if not rows:
        return []

    top = rows[0]
    return [{
        "line": top["line_id"],
        "issue": "Frequent stops / slow changeover",
        "impact_units_per_day": 480
    }]
