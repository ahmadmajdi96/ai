import pandas as pd
import boto3
import os
from common_lib.db import execute

def _get_minio_client():
    endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000").replace("http://","").replace("https://","")
    access = os.getenv("MINIO_ACCESS_KEY")
    secret = os.getenv("MINIO_SECRET_KEY")
    s3 = boto3.client(
        "s3",
        endpoint_url="http://" + endpoint,
        aws_access_key_id=access,
        aws_secret_access_key=secret
    )
    return s3

def parse_s3_uri(uri: str):
    # "s3://bucket/key"
    assert uri.startswith("s3://")
    _, _, rest = uri.partition("s3://")
    bucket, _, key = rest.partition("/")
    return bucket, key

def load_and_normalize_csv(tenant_id: str, s3_path: str, schema_map: dict, table_type: str):
    bucket, key = parse_s3_uri(s3_path)
    s3 = _get_minio_client()
    obj = s3.get_object(Bucket=bucket, Key=key)
    import io
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    df = df.rename(columns=schema_map)

    inserted = 0
    if table_type == "production_events":
        for _, row in df.iterrows():
            execute("""
                INSERT INTO production_events
                (tenant_id, ts, line_id, units_made, defects, downtime_reason)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [
                tenant_id,
                row.get("ts"),
                row.get("line_id"),
                row.get("units_made"),
                row.get("defects"),
                row.get("downtime_reason"),
            ])
            inserted += 1
    return inserted
