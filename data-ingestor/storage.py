from common_lib.db import execute

def store_file_reference(tenant_id: str, s3_path: str, table_type: str):
    execute("""
        INSERT INTO decision_log (tenant_id, decision, result_json)
        VALUES (%s, %s, %s)
    """, [tenant_id, f"uploaded {s3_path} for {table_type}", None])
