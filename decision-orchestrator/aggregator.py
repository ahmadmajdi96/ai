import statistics

def aggregate_ratings(agent_results, tenant_id):
    valid_ratings = []
    for r in agent_results:
        if isinstance(r, dict) and "rating" in r:
            valid_ratings.append(r["rating"])

    if not valid_ratings:
        return {
            "overall_rating": 0,
            "confidence": 0,
            "summary": "No valid agent responses"
        }

    avg_rating = statistics.mean(valid_ratings)
    confidence = 0.8 + 0.05 * len(valid_ratings)
    if avg_rating > 80:
        summary = "Strong decision"
    elif avg_rating > 60:
        summary = "Acceptable but watch risks"
    else:
        summary = "Risky decision"

    return {
        "overall_rating": avg_rating,
        "confidence": round(confidence, 2),
        "summary": summary
    }
