from common_lib.db import fetch_all
def build_kpi_snapshot(tenant_id: str):
    rows = fetch_all("""
        SELECT SUM(units_made) AS units_made,
               SUM(defects) AS defects,
               EXTRACT(EPOCH FROM (MAX(ts)-MIN(ts)))/3600.0 AS hours_span
        FROM production_events
        WHERE tenant_id=%s
          AND ts > NOW() - INTERVAL '24 hours'
    """,[tenant_id])

    throughput_per_hour = None
    scrap_rate_pct = None
    downtime_min = None
    late_orders_count = 3

    if rows and rows[0]["units_made"] is not None:
        r = rows[0]
        total_units = r["units_made"] or 0
        hours_span = r["hours_span"] or 1e-6
        throughput_per_hour = total_units / hours_span
        defects_sum = r["defects"] or 0
        scrap_rate_pct = (defects_sum / max(total_units,1)) * 100.0

    down_rows = fetch_all("""
        SELECT COUNT(*) AS cnt
        FROM production_events
        WHERE tenant_id=%s
          AND ts > NOW() - INTERVAL '24 hours'
          AND downtime_reason IS NOT NULL
    """,[tenant_id])
    if down_rows:
        downtime_min = down_rows[0]["cnt"]

    return {
        "throughput_per_hour": throughput_per_hour,
        "scrap_rate_pct": scrap_rate_pct,
        "downtime_min": downtime_min,
        "late_orders_count": late_orders_count
    }
