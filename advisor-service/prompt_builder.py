import json

def build_advisor_prompt(tenant_id, question, bundle):
    system_prompt = f"""
You are an Operations Advisor AI for tenant {tenant_id}.
You MUST respond with valid JSON only, with keys:
root_cause, short_term_actions, long_term_actions,
risk_if_ignored, kpi_impacts, confidence.
Follow client rules strictly. If unsure, say not sure.
"""
    user_prompt = {
        "QUESTION": question,
        "CONTEXT_BUNDLE": bundle
    }
    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": json.dumps(user_prompt)}
    ]
    return messages
